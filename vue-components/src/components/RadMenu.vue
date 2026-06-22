<template>
  <div ref="outerDiv" class="fullSize">
    <div ref="inerDiv" class="centerAbs" v-show="isOpen" :style="positionStyleMain">
      <slot />
      <div :style="positionStyleCenterButton" class="centerAbs">
        <slot name="central">
          <tooltip-button
            text="Close menu"
            class="radMenuButton"
            icon="mdi-close"
            @click="isOpen = false"
            :color="color"
            :size="closeMenuButtonRadius >= 0 ? 2 * closeMenuButtonRadius : 2 * minRadius"
          />
        </slot>
      </div>
      <div
        v-for="placeholderName in Object.keys(placeholdersPositionStyle)"
        :key="placeholderName"
        :style="placeholdersPositionStyle[placeholderName]"
        class="centerAbs"
      >
        <slot :name="placeholderName">
          <tooltip-button
            v-if="placeholderName == props.dragButtonPosition"
            class="radMenuButton dragZone"
            text="Drag menu"
            location="top"
            icon="mdi-cursor-move"
            @mousedown="startDrag"
            :color="color"
          />
          <tooltip-button
            v-else-if="placeholderName == 'right-top'"
            :text="rightMenuOpen ? 'Close right menu' : 'Open right menu'"
            location="end"
            class="radMenuButton"
            :icon="rightMenuOpen ? 'mdi-chevron-left' : 'mdi-chevron-right'"
            :active="rightMenuOpen"
            @click="rightMenuOpen = !rightMenuOpen"
            :color="color"
          />
        </slot>
      </div>
      <div class="sideDiv" v-show="rightMenuOpen" :style="positionStyleRightMenu">
        <slot name="right-menu" />
      </div>
      <div class="sideDiv" v-show="leftMenuOpen" :style="positionStyleLeftMenu">
        <slot name="left-menu" />
      </div>
      <div class="sideDiv" v-show="upMenuOpen" :style="positionStyleUpMenu">
        <slot name="up-menu" />
      </div>
      <div class="sideDiv" v-show="downMenuOpen" :style="positionStyleDownMenu">
        <slot name="down-menu" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { provide, ref, computed, type ComputedRef } from 'vue'

import type { EightSymmetryPoints, Point } from '@/utils/types'
import TooltipButton from './TooltipButton.vue'
import {
  boxToStyle,
  getEightSymmetryPoints,
  pointToStyle,
  pointToStyleTopRight,
  pointToStyleBottomLeft,
} from '../utils/geometry'
import { applyToValues } from '../utils/dicts'
import { useDraggableContextMenu } from '../composables/useDraggableContextMenu'

// Setup

interface Props {
  openAtRightClickPos: boolean
  closeMenuButtonRadius: number
  color: string
  dragButtonPosition: string
}

const props = withDefaults(defineProps<Props>(), {
  openAtRightClickPos: true,
  closeMenuButtonRadius: -1,
  color: '#7777',
  dragButtonPosition: 'top-right',
})

const isOpen = defineModel<boolean>('open', { default: false })

const rightMenuOpen = defineModel<boolean>('rightmenuopen', { default: false })
const leftMenuOpen = defineModel<boolean>('leftmenuopen', { default: false })
const upMenuOpen = defineModel<boolean>('upmenuopen', { default: false })
const downMenuOpen = defineModel<boolean>('downmenuopen', { default: false })

const pagePos = ref<Point>({ x: 0, y: 0 })

// Use composable that handles open on right click and drag when startDrag is
// called
const outerDiv = ref<HTMLDivElement>()
const innerDiv = ref<HTMLDivElement>()
const { centerPos, startDrag } = useDraggableContextMenu(
  isOpen,
  pagePos,
  outerDiv,
  innerDiv,
  computed(() => props.openAtRightClickPos),
)

// Handle maximum radius and tells it to children components

// radii of all children
const radii = ref<ComputedRef<number>[]>([])

const maxRadius = computed(() => Math.max(...radii.value.map((r) => r.value)))
const minRadius = computed(() => Math.min(...radii.value.map((r) => r.value)))

provide('registerRadius', (radius: ComputedRef<number>) => {
  radii.value.push(radius)
})
provide('unregisterRadius', (radius: ComputedRef<number>) => {
  radii.value = radii.value.filter((item) => item !== radius)
})
provide('maxRadius', maxRadius)

// Position divs

// position the menu in the page at `centerPos`
const positionStyleMain = computed(() => ({
  ...boxToStyle([maxRadius.value * 2, maxRadius.value * 2]),
  ...pointToStyle(centerPos.value),
}))

// position the center button at the center of the menu
const positionStyleCenterButton = computed(() =>
  pointToStyle({ x: maxRadius.value, y: maxRadius.value }),
)

// position the side menus
const positionStyleRightMenu = computed(() => pointToStyle({ x: 2 * maxRadius.value + 20, y: 0 }))
const positionStyleLeftMenu = computed(() =>
  pointToStyleTopRight({ x: 2 * maxRadius.value + 20, y: 0 }),
)
const positionStyleUpMenu = computed(() =>
  pointToStyleBottomLeft({ x: 0, y: 2 * maxRadius.value + 20 }),
)
const positionStyleDownMenu = computed(() => pointToStyle({ x: 0, y: 2 * maxRadius.value + 20 }))

// Position the 8 small placeholders

// (a,b) make the relative coordinates ([-1, 1] as coordinate interval) of the
// first placeholder
const a = 0.95
const b = 0.65

// placeholders position is in [0, maxRadius] coordinate interval
const placeholdersPosition = computed<EightSymmetryPoints>(() =>
  getEightSymmetryPoints(a, b, maxRadius.value),
)
// Get the corresponding CSS style
const placeholdersPositionStyle = computed(() =>
  applyToValues(placeholdersPosition.value, pointToStyle),
)

// Open at cursor position exposed callback

// Always keep track of mouse position in case of openAtCursor call
const cursorPos = ref<Point>({ x: 0, y: 0 })
document.addEventListener('mousemove', (event) => {
  cursorPos.value = { x: event.pageX, y: event.pageY }
})

const openAtCursor = () => {
  isOpen.value = true
  pagePos.value = cursorPos.value
}
defineExpose({
  openAtCursor,
})
</script>

<style scoped>
.centerAbs {
  position: absolute;
  transform: translate(-50%, -50%);
  pointer-events: auto;
}

.fullSize {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.sideDiv {
  position: absolute;
}

.dragZone {
  cursor: grab;
}
.dragZone:active {
  cursor: grabbing;
}
</style>
