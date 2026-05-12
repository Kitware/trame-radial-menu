<template>
  <div class="centerAbs" v-show="isOpen" :style="positionStyleMain">
    <slot />
    <div :style="positionStyleCenterButton" class="centerAbs">
      <slot name="central-button">
        <v-tooltip text="Close menu">
          <template v-slot:activator="{ props: tooltipActivatorProps }">
            <v-btn
              class="radMenuButton"
              v-bind="tooltipActivatorProps"
              icon="mdi-close"
              @click="isOpen = false"
              variant="flat"
              :color="color"
              :size="closeMenuButtonRadius >= 0 ? 2 * closeMenuButtonRadius : 2 * minRadius"
            />
          </template>
        </v-tooltip>
      </slot>
    </div>
    <div v-for="placeholderName in Object.keys(placeholdersPositionStyle)" :key="placeholderName">
      <div :style="placeholdersPositionStyle[placeholderName]" class="centerAbs">
        <div v-if="placeholderName != 'right-bottom' && placeholderName != 'bottom-right'">
          <slot :name="placeholderName" />
        </div>
        <div v-else-if="placeholderName == 'bottom-right'">
          <v-tooltip text="Drag menu">
            <template v-slot:activator="{ props: tooltipActivatorProps }">
              <v-btn
                class="radMenuButton dragZone"
                v-bind="tooltipActivatorProps"
                icon="mdi-cursor-move"
                @mousedown="startDrag"
                :color="color"
                variant="flat"
                size="40"
              />
            </template>
          </v-tooltip>
        </div>
        <div v-else-if="placeholderName == 'right-bottom'">
          <v-tooltip text="Open side menu">
            <template v-slot:activator="{ props: tooltipActivatorProps }">
              <v-btn
                class="radMenuButton"
                v-bind="tooltipActivatorProps"
                :active="sideMenuOpen"
                :icon="sideMenuOpen ? 'mdi-chevron-left' : 'mdi-chevron-right'"
                @click="sideMenuOpen = !sideMenuOpen"
                :color="color"
                variant="flat"
                size="40"
              />
            </template>
          </v-tooltip>
        </div>
      </div>
    </div>
    <div class="sideDiv" v-show="sideMenuOpen" :style="positionStyleSide">
      <slot name="side-menu" />
    </div>
  </div>
</template>

<script setup>
import { provide, ref, computed, defineModel } from 'vue'
import { boxToStyle, getEightSymmetryPoints, pointToStyle } from '../utils/geometry'
import { applyToValues } from '../utils/dicts'
import { useDraggableContextMenu } from '../composables/useDraggableContextMenu'

// Setup

defineProps({
  closeMenuButtonRadius: { type: Number, default: -1 },
  color: { type: String, default: '#77777777' },
})

const sideMenuOpen = defineModel('sidemenuopen', true)
const isOpen = defineModel('open', false)

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

// position the side menu on the right of the menu
const positionStyleSide = computed(() => pointToStyle([2 * maxRadius.value + 20, 0]))

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
