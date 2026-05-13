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
      v-for="placeholderName in ['left-bottom', 'bottom-right', 'right-bottom']"
      :key="placeholderName"
      :style="placeholdersPositionStyle[placeholderName]"
      class="centerAbs"
    >
      <slot :name="placeholderName" />
    </div>
    <div :style="placeholdersPositionStyle['top-right']" class="centerAbs">
      <slot name="top-right">
        <tooltip-button
          class="radMenuButton dragZone"
          text="Drag menu"
          location="top"
          icon="mdi-cursor-move"
          @mousedown="startDrag"
          :color="color"
        />
      </slot>
    </div>
    <div
      v-for="(placeholderProps, placeholderName) in {
        'right-top': [
          rightMenuOpen,
          'mdi-chevron-left',
          'mdi-chevron-right',
          () => {
            rightMenuOpen = !rightMenuOpen
          },
          'end',
        ],
        'left-top': [
          leftMenuOpen,
          'mdi-chevron-right',
          'mdi-chevron-left',
          () => {
            leftMenuOpen = !leftMenuOpen
          },
          'start',
        ],
        'top-left': [
          upMenuOpen,
          'mdi-chevron-down',
          'mdi-chevron-up',
          () => {
            upMenuOpen = !upMenuOpen
          },
          'top',
        ],
        'bottom-left': [
          downMenuOpen,
          'mdi-chevron-up',
          'mdi-chevron-down',
          () => {
            downMenuOpen = !downMenuOpen
          },
          'bottom',
        ],
      }"
      :key="placeholderName"
      :style="placeholdersPositionStyle[placeholderName]"
      class="centerAbs"
    >
      <slot :name="placeholderName">
        <tooltip-button
          text="Open right menu"
          :location="placeholderProps[4]"
          class="radMenuButton"
          :icon="placeholderProps[0] ? placeholderProps[1] : placeholderProps[2]"
          :active="placeholderProps[0]"
          @click="placeholderProps[3]"
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

<script setup>
import { provide, ref, computed, defineModel } from 'vue'
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

defineProps({
  closeMenuButtonRadius: { type: Number, default: -1 },
  color: { type: String, default: '#77777777' },
})

const isOpen = defineModel('open', false)

const rightMenuOpen = defineModel('rightmenuopen', false)
const leftMenuOpen = defineModel('leftmenuopen', false)
const upMenuOpen = defineModel('upmenuopen', false)
const downMenuOpen = defineModel('downmenuopen', false)

// Tell children component they are under a RadMenu so RadWheels throw an error
// if they aren't under a RadMenu
provide('parentRadMenu', () => {})

// Use composable that handles open on right click and drag when startDrag is
// called
const { cx, cy, startDrag } = useDraggableContextMenu(isOpen)

// Handle maximum radius and tells it to children components

// radii of all children
const radii = ref([])

const maxRadius = computed(() => Math.max(...radii.value.map((r) => r.value)))
const minRadius = computed(() => Math.min(...radii.value.map((r) => r.value)))

provide('registerRadius', (radius) => {
  radii.value.push(radius)
})
provide('maxRadius', maxRadius)

// Position divs

// position the menu in the page at (cx, cy)
const positionStyleMain = computed(() => ({
  ...boxToStyle(maxRadius.value * 2, maxRadius.value * 2),
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
const placeholdersPosition = computed(() => getEightSymmetryPoints(a, b, maxRadius.value))
// Get the corresponding CSS style
const placeholdersPositionStyle = computed(() =>
  applyToValues(placeholdersPosition.value, pointToStyle)
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
