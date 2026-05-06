<template>
    <div
        class="centerAbs"
        v-show="isOpen"
        :style="positionStyleMain"
    >

        <slot />

        <div>
            <v-tooltip text="Close menu">
                <template v-slot:activator="{ props: tooltipActivatorProps }">
                    <v-btn
                        class="centerAbs"
                        :style="positionStyleCenterButton"
                        v-bind="tooltipActivatorProps"
                        icon="mdi-close"
                        @click="isOpen = false"
                        :color="color"
                        size="80"
                    />
                </template>
            </v-tooltip>
        </div>

        <div>
            <v-tooltip text="Open side menu">
                <template v-slot:activator="{ props: tooltipActivatorProps }">
                    <v-btn
                        class="centerAbs"
                        :style="positionSwitchSideMenu"
                        v-bind="tooltipActivatorProps"
                        :active="sideMenuOpen"
                        :icon="sideMenuOpen?'mdi-chevron-left':'mdi-chevron-right'"
                        @click="sideMenuOpen = !sideMenuOpen"
                        :color="color"
                        size="40"
                    />
                </template>
            </v-tooltip>
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
    color: {type:String, default: "#7777"}
});

const isOpen = defineModel('open', false);
const sideMenuOpen = defineModel('side_menu_open', true);

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
