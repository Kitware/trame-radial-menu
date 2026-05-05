<template>
    <div
        class="centerAbs"
        v-show="isOpen"
        :style="positionStyleMain"
    >

        <slot />

        <div ref="closeMenuButtonElem">
            <v-tooltip text="Close menu">
                <template v-slot:activator="{ props: tooltipActivatorProps }">
                    <v-btn
                        class="centerAbs"
                        v-bind="tooltipActivatorProps"
                        :style="positionStyleCenterButton"
                        icon="mdi-close"
                        size="80"
                        variant="tonal"
                        @click="isOpen = false"
                    />
                </template>
            </v-tooltip>
        </div>

        <div ref="openSideMenuButtonElem">
            <v-tooltip text="Open side menu">
                <template v-slot:activator="{ props: tooltipActivatorProps }">
                    <v-btn
                        class="centerAbs"
                        v-bind="tooltipActivatorProps"
                        :style="positionSwitchSideMenu"
                        :active="sideMenuOpen"
                        :icon="sideMenuOpen?'mdi-chevron-left':'mdi-chevron-right'"
                        size="40"
                        variant="tonal"
                        @click="sideMenuOpen = !sideMenuOpen"
                    />
                </template>
            </v-tooltip>
        </div>

        <div
            class="sideDiv"
            v-show="sideMenuOpen"
            :style="positionStyleSide"
            ref="sideMenuElem"
        >
            <slot name="side-menu" />
        </div>
    </div>
</template>

<script setup>

import { provide, inject, ref, computed, onMounted, onUnmounted} from 'vue';


// Setup

provide('parentRadMenu', () => {}); // Tell children component they are under a RadMenu



//#region Handle maximum radius and tells it to children components

// radii of all children
const radii = ref([]);

// maximum radii of all children
const maxRadius = computed(() => {
    let max = 0;
    radii.value.forEach((radius) => {
        if (radius.value > max) {
            max = radius.value;
        }
    });
    return max;
});
provide('registerMaxRadius', (radius) => {
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

// position the switch to open side menu on the bottom right of the menu
const positionSwitchSideMenu = computed(() => ({
    left: `${maxRadius.value * 1.85}px`,
    top: `${maxRadius.value * 1.85}px`,
}))
//#endregion



//#region Handle click and isOpen

const isOpen = ref(false); // true if the menu must be shown
const sideMenuOpen = ref(true); // true if the side menu must be shown

const closeMenu = () => {isOpen.value = false};
defineExpose({ closeMenu }); // for parents to close it
provide('closeMenu', closeMenu); // for children to close it

//#region List of elements to ignore when clicking outside the menu to close it

// Elements from parents
const clickIgnoreElemsParent = inject('avoidElems', []);

// Elements from <slot />
const clickIgnoreElemsChildren = ref([]);
provide('registerClickAvoidElem', (elem) => {clickIgnoreElemsChildren.value.push(elem);});

// Element from this template
const closeMenuElem = ref(null);
const openSideMenuElem = ref(null);
const sideMenuElem = ref(null);
const clickIgnoreElemsTemplate = [
    closeMenuButtonElem,
    openSideMenuButtonElem,
    sideMenuElem,
]

// All
const clickIgnoreElems = computed(()=>[...clickIgnoreElemsParent, ...clickIgnoreElemsChildren.value, ...clickIgnoreElemsTemplate]);
//#endregion

const rightClick = (event) => {
    event.preventDefault();
    isOpen.value = true; cx.value = event.pageX; cy.value = event.pageY;
}
const leftClick = (event) => {
    if (
        !clickIgnoreElems.value.some((elem) => elem.value.contains(event.target))
    ) {
        if (isOpen.value) {isOpen.value = false;}
    }
}


onMounted(() => {
    document.addEventListener('mousedown', leftClick);
    document.addEventListener('contextmenu', rightClick);
});

onUnmounted(() => {
  document.removeEventListener('mousedown', leftClick);
  document.removeEventListener('contextmenu', rightClick);
});
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

</style>
