<template>
    <div :style="positionStyle" ref="itemElem">
        <slot />
    </div>
</template>
<script setup>

import { inject, computed, onMounted, ref, onUnmounted } from 'vue';
import { polar } from '@/utils/geometry.js';


// ### Setup

const props = defineProps({
    label: {type: String, default: ''},
    icon: {type: String, default: ''},
    size: {type: Number, default: 1},
    closeOnClick: {type: Boolean, default: true},
})

const emit = defineEmits([
    'click'
]);

inject('parentRadWheel', () => {throw new Error("RadItem must be under a RadWheel");})();



// ### Registers

const itemElem = ref(null);
inject('registerClickAvoidElem')(itemElem);

const sizeRef = computed(()=>props.size);
const [beginAngle, endAngle] = inject('registerSize')(sizeRef);
const midAngle = computed(()=>(beginAngle.value + endAngle.value)/2)
const [innerRadius, outerRadius] = inject('innerAndOuterRadii');
inject('registerMaxRadius')(outerRadius);
const menu_cx = inject('maxRadius');
const menu_cy = menu_cx;


// ### Calculates angles, radii and positions

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


</script>
<style scoped>
</style>
