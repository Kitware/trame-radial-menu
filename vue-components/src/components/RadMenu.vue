<template>
  <div class="centerAbs" v-show="isOpen" :style="positionStyleMain">
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
          v-if="placeholderName == 'right-top'"
          text="Open side menu"
          location="end"
          class="radMenuButton"
          :icon="rightMenuOpen ? 'mdi-chevron-left' : 'mdi-chevron-right'"
          :active="rightMenuOpen"
          @click="rightMenuOpen = !rightMenuOpen"
          :color="color"
        />
        <tooltip-button
          v-if="placeholderName == 'top-right'"
          class="radMenuButton dragZone"
          text="Drag menu"
          location="top"
          icon="mdi-cursor-move"
          @mousedown="startDrag"
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
</template>

<script setup lang="ts">
import { provide, ref, computed, type ComputedRef } from 'vue'

import type { EightSymmetryPoints } from '@/utils/types'
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

withDefaults(
  defineProps<{
    closeMenuButtonRadius: number
    color: string
  }>(),
  {
    closeMenuButtonRadius: -1,
    color: '#7777',
  },
)
const isOpen = defineModel<boolean>('open', { default: false })

const rightMenuOpen = defineModel('rightmenuopen', { default: false })
const leftMenuOpen = defineModel('leftmenuopen', { default: false })
const upMenuOpen = defineModel('upmenuopen', { default: false })
const downMenuOpen = defineModel('downmenuopen', { default: false })
// Tell children component they are under a RadMenu so RadWheels throw an error
// if they aren't under a RadMenu
provide('parentRadMenu', () => {})

// Use composable that handles open on right click and drag when startDrag is
// called
const { cx, cy, startDrag } = useDraggableContextMenu(isOpen)

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

// position the menu in the page at (cx, cy)
const positionStyleMain = computed(() => ({
  ...boxToStyle([maxRadius.value * 2, maxRadius.value * 2]),
  ...pointToStyle([cx.value, cy.value]),
}))

// position the center button at the center of the menu
const positionStyleCenterButton = computed(() => pointToStyle([maxRadius.value, maxRadius.value]))

// position the side menus
const positionStyleRightMenu = computed(() => pointToStyle([2 * maxRadius.value + 20, 0]))
const positionStyleLeftMenu = computed(() => pointToStyleTopRight([2 * maxRadius.value + 20, 0]))
const positionStyleUpMenu = computed(() => pointToStyleBottomLeft([0, 2 * maxRadius.value + 20]))
const positionStyleDownMenu = computed(() => pointToStyle([0, 2 * maxRadius.value + 20]))

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
</script>

<style scoped>
.centerAbs {
  position: absolute;
  transform: translate(-50%, -50%);
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
