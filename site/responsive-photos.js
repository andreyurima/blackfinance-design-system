// SVG image elements have no native srcset. Keep their approved masks and geometry.
for (const image of document.querySelectorAll('image[data-responsive-sources]')) {
  const candidates = image.dataset.responsiveSources.split(',').map(value => {
    const [src, width] = value.trim().split(/\s+/)
    return { src, width: Number.parseInt(width, 10) }
  })
  let visible = false
  const choose = () => {
    if (!visible) return
    const box = image.getBoundingClientRect()
    const width = Math.max(box.width, box.height * Number(image.dataset.photoRatio))
    const required = width * (window.devicePixelRatio || 1)
    const selected = candidates.find(candidate => candidate.width >= required) ?? candidates.at(-1)
    if (selected && image.getAttribute('href') !== selected.src) image.setAttribute('href', selected.src)
  }
  const observer = new IntersectionObserver(entries => {
    if (entries.some(entry => entry.isIntersecting)) {
      visible = true
      choose()
      observer.disconnect()
    }
  }, { rootMargin: '300px' })
  observer.observe(image)
  const resize = new ResizeObserver(choose)
  resize.observe(image)
  image.addEventListener('error', () => {
    if (image.getAttribute('href') !== image.dataset.originalHref) {
      visible = false
      resize.disconnect()
      image.setAttribute('href', image.dataset.originalHref)
    }
  })
}
