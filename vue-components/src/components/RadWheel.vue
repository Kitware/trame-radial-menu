<template>
    <svg :width="maxRadius * 2" :height="maxRadius * 2">
        <path
            :d="donutPath"
            :fill="props.color"
            :fill-rule="evenodd"
        />
    </svg>
    <div ref="slotElem">
        <slot />
    </div>
</template>

<script setup>

import { provide, inject, ref, computed } from 'vue';


// Setup

const props = defineProps({
    innerRadius: { type: Number, default: -1 },
    outerRadius: { type: Number, default: -1 },
    beginAngle: { type: Number, default: 0 },
    endAngle: { type: Number, default: 360 },
    color: {type: String, default: '#7777'},
});

provide('parentRadWheel', () => {}); // Tell children component they are under a RadWheel
inject('parentRadMenu', () => {throw new Error("RadWheel must be under a RadMenu");})();



//#region Handle inner and outer radii

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
//#endregion



//#region Registers

// Radius
inject('registerRadius')(innerRadius);
inject('registerRadius')(outerRadius);
//#endregion



// Draw the donut
const donutPath = computed(() => {
    return `
        M ${maxRadius.value - outerRadius.value},${maxRadius.value}
        A ${outerRadius.value} ${outerRadius.value} 0 1 1 ${maxRadius.value + outerRadius.value},${maxRadius.value}
        A ${outerRadius.value} ${outerRadius.value} 0 1 1 ${maxRadius.value - outerRadius.value},${maxRadius.value}
        M ${maxRadius.value - innerRadius.value},${maxRadius.value}
        A ${innerRadius.value} ${innerRadius.value} 0 1 0 ${maxRadius.value + innerRadius.value},${maxRadius.value}
        A ${innerRadius.value} ${innerRadius.value} 0 1 0 ${maxRadius.value - innerRadius.value},${maxRadius.value}
        Z
    `;
});



//#region Handle angles and sizes of items

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
//#endregion
</script>

<style scoped>
svg {
    pointer-events: none;
    position: absolute;
    transform: 'translate(-50%, -50%)',
}
</style>
