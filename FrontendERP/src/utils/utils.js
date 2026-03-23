// Formatea fechas: "2024-01-15" → "15/01/2024"
export function f_Format(value) {
  if (!value) return ''
  const date = new Date(value)
  if (!isNaN(date)) {
    return date.toLocaleDateString('es-PE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    })
  }
  return value
}