<template>
    <div :style="positionStyle">
        <v-tooltip
            v-if="tooltipLabel != ''"
            :text="tooltipLabel"
            :location="location"
        >
            <template v-slot:activator="{ props }">
                <div v-bind="props">
                    <slot />
                </div>
            </template>
        </v-tooltip>
        <div v-else>
            <slot />
        </div>
    </div>
</template>
<script setup>

import { inject, computed, onUnmounted } from 'vue';
import { polar } from '@/utils/geometry.js';


// Setup

const props = defineProps({
    size: {type: Number, default: 1},
    tooltipLabel: {type: String, default: ''}
});

inject('parentRadWheel', () => {throw new Error("RadItem must be under a RadWheel");})();



//#region Registers

const sizeRef = computed(()=>props.size);
const [beginAngle, endAngle] = inject('registerSize')(sizeRef);
const [innerRadius, outerRadius] = inject('innerAndOuterRadii');
const menu_cx = inject('maxRadius');
const menu_cy = menu_cx;
//#endregion



//#region Calculates angles, radii and positions

const midAngle = computed(()=>(beginAngle.value + endAngle.value)/2)
const lambdaRadius = (lambda) => (innerRadius.value + (outerRadius.value - innerRadius.value) * lambda);
const iconRadius = 0.5;
const center_point = computed(() => polar(menu_cx.value, menu_cy.value, lambdaRadius(iconRadius), midAngle.value));

const positionStyle = computed(() => ({
    position: 'absolute',
    left: `${center_point.value.x}px`,
    top: `${center_point.value.y}px`,
    transform: 'translate(-50%, -50%)',
}));

onUnmounted(() => {
    inject("unregisterSize")(sizeRef);
});
//#endregion



//#region Tooltip position

const location = computed(()=>
    midAngle.value >  45 && midAngle.value <= 135 ? "end"    :
    midAngle.value > 135 && midAngle.value <= 225 ? "bottom" :
    midAngle.value > 225 && midAngle.value <= 315 ? "start"  :
                                                    "top"
);
//#endregion

</script>
<style scoped>
</style>
