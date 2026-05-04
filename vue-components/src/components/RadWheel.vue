<template>
    <svg :width="maxRadius * 2" :height="maxRadius * 2">
        <circle
            :cx="maxRadius" :cy="maxRadius" :r="outerRadius"
            :fill="props.color"
        />
    </svg>
    <div ref="slotElem">
        <slot />
    </div>
</template>

<script setup>

import { provide, inject, ref, computed } from 'vue';


// ### Setup

const props = defineProps({
    innerRadius: { type: Number, default: -1 },
    outerRadius: { type: Number, default: -1 },
    beginAngle: { type: Number, default: 0 },
    endAngle: { type: Number, default: 360 },
    color: {type: String, default: '#aaa5'},
});

provide('parentRadWheel', () => {}); // Tell children component they are under a RadWheel
inject('parentRadMenu', () => {throw new Error("RadWheel must be under a RadMenu");})();



// ### Handle inner and outer radii

const parentInnerAndOuterRadii = inject('innerAndOuterRadii', null);
const innerRadius = computed(() => {
    if (props.innerRadius >= 0)
        return props.innerRadius;
    else if (parentInnerAndOuterRadii != null)
        return parentInnerAndOuterRadii[1].value;
    else return 40;
});
const outerRadius = computed(() => {
    if (props.outerRadius >= 0)
        return props.outerRadius;
    else if (parentInnerAndOuterRadii != null)
        return innerRadius.value + 60;
    else return 100;
});

provide('innerAndOuterRadii', [innerRadius, outerRadius]);
const maxRadius = inject('maxRadius');



// ### Registers

// Radius
inject('registerMaxRadius')(outerRadius);



// ### Handle angles and sizes of items

const totalAngle = computed(()=>props.endAngle - props.beginAngle);
const sizes = ref([]);
const cumulSizes = computed(() => {
    let res = [0];
    sizes.value.forEach((element)=>{
        res.push(res.at(-1) + element.value);
    })
    return res;
});
const totalSize = computed(() =>
    cumulSizes.value.at(-1)
);
provide('registerSize',
    (size)=>{
        sizes.value.push(size);
        let childId = computed(()=>{
            let res = 0;
            sizes.value.forEach((elem, i) => {
                if (elem===size) {res = i}
            });
            return res;
        });
        let cumulSizeBegin = computed(() => cumulSizes.value.at(childId.value));
        let cumulSizeEnd = computed(() => cumulSizes.value.at(childId.value + 1));
        let beginAngle = computed(() =>
            props.beginAngle + (totalAngle.value / totalSize.value) * (cumulSizeBegin.value) - totalAngle.value / (2*totalSize.value)
        );
        let endAngle = computed(() =>
            props.beginAngle + (totalAngle.value / totalSize.value) * (cumulSizeEnd.value) - totalAngle.value / (2*totalSize.value)
        );
        return [
            beginAngle,
            endAngle
        ];
    }
);

provide('unregisterSize', (size)=>{
    sizes.value = sizes.value.filter(item => item !== size)
})
</script>

<style scoped>
svg {
    pointer-events: none;
    position: absolute;
    transform: 'translate(-50%, -50%)',
}
</style>
