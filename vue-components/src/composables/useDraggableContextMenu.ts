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
  initialMouseX: number
  initialMouseY: number
}

export function useDraggableContextMenu(
  isOpen: Ref<boolean>,
  containerDiv: Ref<HTMLDivElement | undefined>,
  innerDiv: Ref<HTMLDivElement | undefined>,
): {
  centerPos: ComputedRef<Point>
  startDrag: (event: MouseEvent) => void
} {
  // Click position on the page
  const clickPos = ref<Point>([0, 0])

  // Container BBox in page coordinate
  const containerRect: ComputedRef<BBox> = computed(() =>
    translateBBox(containerDiv.value!.getBoundingClientRect(), [window.scrollX, window.scrollY]),
  )

  const centerPos = computed(() => clampPosition(clickPos.value))

  let dragState: DragState = {
    isDragging: false,
    startPos: [0, 0],
    initialMouseX: 0,
    initialMouseY: 0,
  }

  // Clamp a position so the BBox around children elements fits in containerDiv
  const clampPosition = (newPos: Point): Point => {
    if (!containerDiv.value) {
      return newPos
    }
    const bboxes: BBox[] = Array.from(innerDiv.value!.querySelectorAll('*'))
      .map((el) => el.getBoundingClientRect())
      .map(domRectToBBox)
      .filter(hasNonZeroArea) // bboxes of children elements in viewport's coordinates
      .map((bbox: BBox) => translateBBox(bbox, [window.scrollX, window.scrollY])) //in page's coordinates
      .map((bbox: BBox) =>
        translateBBox(bbox, [-containerRect.value.left, -containerRect.value.top]),
      ) // in container's div coordinates
    if (bboxes.length == 0) return newPos

    const bbox = bboxes.reduce(bBoxUnion)
    const minX = centerPos.value[0] - bbox.left
    const minY = centerPos.value[1] - bbox.top
    const maxX = BBoxWidth(containerRect.value) - (bbox.right - centerPos.value[0])
    const maxY = BBoxHeight(containerRect.value) - (bbox.bottom - centerPos.value[1])

    const [newX, newY] = newPos
    return [Math.min(maxX, Math.max(minX, newX)), Math.min(maxY, Math.max(minY, newY))]
  }

  // Moves the menu by the delta between the current mouse position and where the drag originally
  // started
  const onDrag = (event: MouseEvent): void => {
    if (!dragState.isDragging) return

    const dx = event.pageX - dragState.initialMouseX
    const dy = event.pageY - dragState.initialMouseY

    clickPos.value = [dragState.startPos[0] + dx, dragState.startPos[1] + dy]
  }

  const stopDrag = (): void => {
    dragState.isDragging = false
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
  }

  const startDrag = (event: MouseEvent): void => {
    dragState = {
      isDragging: true,
      startPos: centerPos.value,
      initialMouseX: event.pageX,
      initialMouseY: event.pageY,
    }

    window.addEventListener('mousemove', onDrag)
    window.addEventListener('mouseup', stopDrag)
    event.preventDefault()
  }

  // Opens the context menu at the cursor position when the user right-clicks
  const rightClick = (event: MouseEvent): void => {
    event.preventDefault()
    isOpen.value = true
    console.log(event.pageX - containerRect.value.left, event.pageY - containerRect.value.top)
    clickPos.value = [event.pageX - containerRect.value.left, event.pageY - containerRect.value.top]
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
