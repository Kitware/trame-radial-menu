<template>
    <div
        class="centerAbs"
        v-show="isOpen"
        :style="positionStyleMain"
    >

        <slot />

        <div
            :style="positionStyleCenterButton"
            class="centerAbs"
        >
            <v-tooltip v-if="closeMenuButton" text="Close menu">
                <template v-slot:activator="{ props: tooltipActivatorProps }">
                    <v-btn
                        class="radMenuButton"
                        v-bind="tooltipActivatorProps"
                        icon="mdi-close"
                        @click="isOpen = false"
                        variant="flat"
                        :color="color"
                        :size="2*minRadius"
                    />
                </template>
            </v-tooltip>
            <div v-else>
                <slot name="central-button"></slot>
            </div>
        </div>
        <div v-for="placeholderName in Object.keys(placeholders)" :key="placeholderName">
            <div
                :style="placeholdersPosition[placeholderName]"
                class="centerAbs"
            >
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
                                :icon="sideMenuOpen?'mdi-chevron-left':'mdi-chevron-right'"
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
        <div
            class="sideDiv"
            v-show="sideMenuOpen"
            :style="positionStyleSide"
        >
            <slot name="side-menu" />
        </div>
    </div>
</template>

<script setup>

import { provide, ref, computed, onMounted, onUnmounted, defineModel} from 'vue';


// Setup

const props = defineProps({
    closeMenuButton: {type:Boolean, default: true},
    closeMenuButtonRadius: {type: Number, default: -1},
    color: {type:String, default: "#77777777"},
});

const sideMenuOpen = defineModel('sidemenuopen', true);
const isOpen = defineModel('open', false);

provide('parentRadMenu', () => {}); // Tell children component they are under a RadMenu



//#region Handle maximum radius and tells it to children components

// radii of all children
const radii = ref([]);

const maxRadius = computed(() => Math.max(...radii.value.map(r => r.value)));
const minRadius = computed(() => Math.min(...radii.value.map(r => r.value)));

provide('registerRadius', (radius) => {
    radii.value.push(radius);
});
provide('maxRadius', maxRadius);
//#endregion



//#region Position elements

// page coordinates of mouse right click
const cx = ref(0); const cy = ref(0);

// position the manu in the page at (cx, cy)
const positionStyleMain = computed(() => ({
    left: `${cx.value}px`,
    top: `${cy.value}px`,
    width: `${maxRadius.value * 2}px`,
    height: `${maxRadius.value * 2}px`,
}))

// position the center button at the center of the menu
const positionStyleCenterButton = computed(() => ({
    left: `${maxRadius.value}px`,
    top: `${maxRadius.value}px`,
}))

// position the side menu on the right of the menu
const positionStyleSide = computed(() => ({
    left: `${2 * maxRadius.value + 20}px`,
    top: `0px`,
}))

// position the 8 small placeholders
const a = 0.95; const b = 0.65;
const placeholders = {
    "right-bottom": [1+a, 1+b],
    "bottom-right": [1+b, 1+a],
    "bottom-left": [1-b, 1+a],
    "left-bottom": [1-a, 1+b],
    "left-top": [1-a, 1-b],
    "top-left": [1-b, 1-a],
    "top-right": [1+b, 1-a],
    "right-top": [1+a, 1-b]
};

const placeholdersPosition = computed(() => {
    let res = {};
    for (let key in placeholders) {
        let [x, y] = placeholders[key];
        res[key] = {
            left: `${maxRadius.value * x}px`,
            top: `${maxRadius.value * y}px`
        }
    }
    return res;
});
//#endregion



//#region Right click opens menu at cursor position
const rightClick = (event) => {
    event.preventDefault();
    isOpen.value = true; cx.value = event.pageX; cy.value = event.pageY;
}

onMounted(() => {
    document.addEventListener('contextmenu', rightClick);
});

onUnmounted(() => {
  document.removeEventListener('contextmenu', rightClick);
});
//#endregion



//#region Drag menu
const isDragging = ref(false)
const startX = ref(0); const startY = ref(0);
const initialMouseX = ref(0); const initialMouseY = ref(0);

const startDrag = (event) => {
    isDragging.value = true;
    startX.value = cx.value;
    startY.value = cy.value;
    initialMouseX.value = event.pageX;
    initialMouseY.value = event.pageY;
    window.addEventListener('mousemove', onDrag);
    window.addEventListener('mouseup', stopDrag);
    event.preventDefault;
}

const onDrag = (event) => {
    if (!isDragging.value) return
    let dx = event.pageX - initialMouseX.value
    let dy = event.pageY - initialMouseY.value
    cx.value = startX.value + dx
    cy.value = startY.value + dy
}

const stopDrag = () => {
    isDragging.value = false
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
}
//#endregion
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
