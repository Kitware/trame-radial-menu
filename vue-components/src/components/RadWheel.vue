<template>
  <svg :width="maxRadius * 2" :height="maxRadius * 2">
    <path :d="donutPath" :fill="props.color" />
  </svg>
  <div ref="slotElem">
    <slot />
  </div>
</template>

<script setup>
import { provide, inject, ref, computed } from 'vue'
import { donutSlicePath, thisBeginAndEndAnglesFromSizes } from '../utils/geometry'

// Setup

const props = defineProps({
  innerRadius: { type: Number, default: -1 },
  outerRadius: { type: Number, default: -1 },
  beginAngle: { type: Number, default: 0 },
  endAngle: { type: Number, default: 360 },
  color: { type: String, default: '#7777' },
})

// Tell children component they are under a RadWheel so RadItems throw an error
// if they aren't under a RadWheel
provide('parentRadWheel', () => {})

// Throw an error if not under a RadMenu
inject('parentRadMenu', () => {
  throw new Error('RadWheel must be under a RadMenu')
})()

// Handle inner and outer radii

const parentInnerAndOuterRadii = inject('innerAndOuterRadii', null)
const innerRadius = computed(() => {
  if (props.innerRadius >= 0) return props.innerRadius
  else if (parentInnerAndOuterRadii != null)
    // inner radius is parent wheel's outer radius
    return parentInnerAndOuterRadii[1].value
  else return 40
})
const outerRadius = computed(() => {
  if (props.outerRadius >= 0) return props.outerRadius
  else return innerRadius.value + 60
})

provide('innerAndOuterRadii', [innerRadius, outerRadius])
const maxRadius = inject('maxRadius')

// Registers radii
inject('registerRadius')(innerRadius)
inject('registerRadius')(outerRadius)

// Handle angles and sizes of items

// Registered sizes of RadItem children
const sizes = ref([])

// Reactive cumulated sum of sizes
const cumulSizes = computed(() => {
  const cumulSizes = [0]
  sizes.value.forEach((element) => {
    cumulSizes.push(cumulSizes.at(-1) + element.value)
  })
  return cumulSizes
})

// Reactive sum of all sizes
const totalSize = computed(() => cumulSizes.value.at(-1))

// When a children registers its size, it gets a ref of its computed begin and
// end angles
provide('registerSize', (size) => {
  sizes.value.push(size)
  const childId = computed(() => sizes.value.findIndex((elem) => elem === size))
  const cumulSizeBegin = computed(() => cumulSizes.value.at(childId.value))
  const cumulSizeEnd = computed(() => cumulSizes.value.at(childId.value + 1))

  return computed(() =>
    thisBeginAndEndAnglesFromSizes(
      props.beginAngle,
      props.endAngle,
      totalSize.value,
      cumulSizeBegin.value,
      cumulSizeEnd.value
    )
  )
})

provide('unregisterSize', (size) => {
  sizes.value = sizes.value.filter((item) => item !== size)
})

// Draw the donut
const donutPath = computed(() =>
  donutSlicePath(
    maxRadius.value,
    maxRadius.value,
    innerRadius.value,
    outerRadius.value,
    props.beginAngle,
    props.endAngle,
    totalSize.value
  )
)
</script>

<style scoped>
svg {
  pointer-events: none;
  position: absolute;
  transform: 'translate(-50%, -50%)';
}
</style>
