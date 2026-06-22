import { ref, onMounted, onUnmounted, computed, type Ref, type ComputedRef } from 'vue'
import {
  hasNonZeroArea,
  domRectToBBox,
  bBoxUnion,
  translateBBox,
  BBoxWidth,
  BBoxHeight,
} from '@/utils/dom'
import type { BBox, Point } from '@/utils/types'

interface DragState {
  isDragging: boolean
  startPos: Point
  initialMouse: Point
}

export function useDraggableContextMenu(
  isOpen: Ref<boolean>,
  pagePos: Ref<Point>,
  containerDiv: Ref<HTMLDivElement | undefined>,
  innerDiv: Ref<HTMLDivElement | undefined>,
  openAtRightClick: Ref<boolean> = ref(true),
): {
  centerPos: ComputedRef<Point>
  startDrag: (event: MouseEvent) => void
} {
  // Container BBox in page coordinate
  const getContainerRect = (): BBox => {
    if (!containerDiv.value) return { left: 0, top: 0, right: 0, bottom: 0 }
    return translateBBox(containerDiv.value.getBoundingClientRect(), {
      x: window.scrollX,
      y: window.scrollY,
    })
  }

  // Click position on the page
  const clickPos: ComputedRef<Point> = computed(() => ({
    x: pagePos.value.x - getContainerRect().left,
    y: pagePos.value.y - getContainerRect().top,
  }))

  const centerPos = computed(() => clampPosition(clickPos.value))

  // Clamp a position so the BBox around children elements fits in containerDiv
  const clampPosition = (newPos: Point): Point => {
    if (!containerDiv.value || !innerDiv.value) return newPos
    if (!hasNonZeroArea(getContainerRect())) return newPos
    const bboxes: BBox[] = Array.from(innerDiv.value!.querySelectorAll('*'))
      .map((el) => el.getBoundingClientRect())
      .map(domRectToBBox)
      .filter(hasNonZeroArea) // bboxes of children elements in viewport's coordinates
      .map((bbox: BBox) => translateBBox(bbox, { x: window.scrollX, y: window.scrollY })) //in page's coordinates
      .map((bbox: BBox) =>
        translateBBox(bbox, { x: -getContainerRect().left, y: -getContainerRect().top }),
      ) // in container's div coordinates
    if (bboxes.length == 0) return newPos

    const bbox = bboxes.reduce(bBoxUnion)
    const upperLeftX = centerPos.value.x - bbox.left
    const upperLeftY = centerPos.value.y - bbox.top
    const lowerRightX = BBoxWidth(getContainerRect()) - (bbox.right - centerPos.value.x)
    const lowerRightY = BBoxHeight(getContainerRect()) - (bbox.bottom - centerPos.value.y)

    const newX = newPos.x
    const newY = newPos.y
    return {
      x: Math.min(lowerRightX, Math.max(upperLeftX, newX)),
      y: Math.min(lowerRightY, Math.max(upperLeftY, newY)),
    }
  }

  let dragState: DragState = {
    isDragging: false,
    startPos: { x: 0, y: 0 },
    initialMouse: { x: 0, y: 0 },
  }

  // Moves the menu by the delta between the current mouse position and where the drag originally
  // started
  const onDrag = (event: MouseEvent): void => {
    if (!dragState.isDragging) return

    const dx = event.pageX - dragState.initialMouse.x
    const dy = event.pageY - dragState.initialMouse.y
    pagePos.value = { x: dragState.startPos.x + dx, y: dragState.startPos.y + dy }
  }

  const stopDrag = (): void => {
    dragState.isDragging = false
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
  }

  const startDrag = (event: MouseEvent): void => {
    dragState = {
      isDragging: true,
      startPos: { x: pagePos.value.x, y: pagePos.value.y },
      initialMouse: { x: event.pageX, y: event.pageY },
    }

    window.addEventListener('mousemove', onDrag)
    window.addEventListener('mouseup', stopDrag)
    event.preventDefault()
  }

  // Opens the context menu at the cursor position when the user right-clicks
  const rightClick = (event: MouseEvent): void => {
    if (openAtRightClick.value) {
      event.preventDefault()
      isOpen.value = true
      pagePos.value = { x: event.pageX, y: event.pageY }
    }
  }

  onMounted(() => {
    document.addEventListener('contextmenu', rightClick)
  })

  onUnmounted(() => {
    document.removeEventListener('contextmenu', rightClick)
    stopDrag()
  })
  return { centerPos, startDrag }
}
