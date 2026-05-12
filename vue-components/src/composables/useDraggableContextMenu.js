import { ref, onMounted, onUnmounted } from 'vue'

export function useDraggableContextMenu(isOpen) {
  // Current position of the context menu on the page
  const cx = ref(0)
  const cy = ref(0)

  let dragState = {
    isDragging: false,
    startX: 0,
    startY: 0,
    initialMouseX: 0,
    initialMouseY: 0,
  }

  // Moves the menu by the delta between the current mouse position
  // and where the drag originally started
  const onDrag = (event) => {
    if (!dragState.isDragging) return

    const dx = event.pageX - dragState.initialMouseX
    const dy = event.pageY - dragState.initialMouseY

    cx.value = dragState.startX + dx
    cy.value = dragState.startY + dy
  }

  const stopDrag = () => {
    dragState.isDragging = false
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
  }

  const startDrag = (event) => {
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
  const rightClick = (event) => {
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
