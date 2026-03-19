export function f_Format(value, decimals = 2) {
  if (value === null || value === undefined || value === '') return ''
  const num = Number(value)
  if (Number.isNaN(num)) return String(value)
  return num.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
}
