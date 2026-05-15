import { ref, onMounted, onUnmounted, type Ref } from 'vue'

interface DragState {
  isDragging: boolean
  startX: number
  startY: number
  initialMouseX: number
  initialMouseY: number
}

export function useDraggableContextMenu(isOpen: Ref<boolean>): {
  cx: Ref<number>
  cy: Ref<number>
  startDrag: (event: MouseEvent) => void
} {
  // Current position of the context menu on the page
  const cx = ref<number>(0)
  const cy = ref<number>(0)

  let dragState: DragState = {
    isDragging: false,
    startX: 0,
    startY: 0,
    initialMouseX: 0,
    initialMouseY: 0,
  }

  // Moves the menu by the delta between the current mouse position
  // and where the drag originally started
  const onDrag = (event: MouseEvent): void => {
    if (!dragState.isDragging) return

    const dx = event.pageX - dragState.initialMouseX
    const dy = event.pageY - dragState.initialMouseY

    cx.value = dragState.startX + dx
    cy.value = dragState.startY + dy
  }

  const stopDrag = (): void => {
    dragState.isDragging = false
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
  }

  const startDrag = (event: MouseEvent): void => {
    dragState = {
      isDragging: true,
      startX: cx.value,
      startY: cy.value,
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
    cx.value = event.pageX
    cy.value = event.pageY
  }

  onMounted(() => {
    document.addEventListener('contextmenu', rightClick)
  })

  onUnmounted(() => {
    document.removeEventListener('contextmenu', rightClick)
    stopDrag()
  })

  return { cx, cy, startDrag }
}
