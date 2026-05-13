<template>
  <v-tooltip :text="tooltipText" :location="location">
    <template v-slot:activator="{ props: tooltipActivatorProps }">
      <v-btn v-bind="compute_v_bind(tooltipActivatorProps)" :size="size" variant="flat" />
    </template>
  </v-tooltip>
</template>

<script setup>
import { useAttrs } from 'vue'

defineProps({
  tooltipText: { type: String, default: '' },
  location: { type: String, default: 'end' },
  size: { type: Number, default: 40 },
})

const attrs = useAttrs()

const compute_v_bind = (tooltipProps) => ({ ...attrs, ...tooltipProps })
</script>
