/*
Utils for encoding KOEI-TW

  <---      orderToKOEITw()      cns11643ToOrder()       unicodeToCNS11643()  <---

  [KOEI-Tw] <----------> [order] <----------> [CNS11643] <----------> [Unicode]

  --->      koeiTwToOrder()      orderToCNS11643()       cns11643ToUnicode()  --->

Expression Formats:
  [KOEI-Tw]:    Uint8Array(2)
  [order]:      int
  [CNS11643]:   str, in "1-2121", "2-2121" like format
  [Unicode]:    str, a character of unicode string

Shortcuts:
  orderOfUnicode()
  orderToUnicode()
*/

import {
  unicodeToCNS11643OrderTable,
  cns11643ToUnicodeTable,
  orderToUnicodeTable
} from './encoding-table.js'

/**
 * Converts an order number to a KOEI Tw-encoded Uint8Array.
 *
 * @param {number} order - The order number to convert.
 * @return {Uint8Array} A Uint8Array representing the KOEI Tw-encoded version
 * of the order number.
 */
export function orderToKOEITw (order) {
  if (order < 0) {
    return new Uint8Array([0x00, 0x00])
  }

  order += 94 // Hi[0x92] starts from 94
  const hiOffset = Math.floor(order / 188)
  const loOffset = order % 188
  const hi = hiOffset + 0x92
  let lo = -1
  if (loOffset >= 0 && loOffset < 10) {
    lo = 0x30 + loOffset
  } else if (loOffset >= 10 && loOffset < 36) {
    lo = 0x41 + loOffset - 10
  } else if (loOffset >= 36 && loOffset < 62) {
    lo = 0x61 + loOffset - 36
  } else if (loOffset >= 62) {
    lo = 0x80 + loOffset - 62
  }

  if (lo === -1) {
    return new Uint8Array([0x00, 0x00])
  }

  return new Uint8Array([hi, lo])
}

/**
 * Converts a Koei TW code to an order number.
 *
 * @param {number|Uint8Array} code - The Koei TW code to convert.
 * @return {number} The order number or -1 if the code is invalid.
 */
export function koeiTwToOrder (code) {
  if (typeof code === 'number') {
    code = new Uint8Array([code / 256, code % 256])
  }

  if (code.length !== 2) {
    return -1
  }

  const hi = code[0]
  const lo = code[1]
  let offset
  let hiBase

  if (hi === 0x92) {
    offset = -94
    hiBase = 0x92
  } else if (hi > 0x92 && hi < 0xd9) {
    offset = 94
    hiBase = 0x93
  } else {
    return -1
  }

  if (lo >= 0x30 && lo <= 0x39) {
    return offset + (hi - hiBase) * 188 + lo - 0x30
  }

  if (lo >= 0x41 && lo <= 0x5a) {
    return offset + (hi - hiBase) * 188 + lo - 0x41 + 10
  }

  if (lo >= 0x61 && lo <= 0x7a) {
    return offset + (hi - hiBase) * 188 + lo - 0x61 + 36
  }

  if (lo >= 0x80 && lo <= 0xfd) {
    return offset + (hi - hiBase) * 188 + lo - 0x80 + 62
  }

  return -1
}

/**
 * Converts a CNS11643 code to its corresponding order.
 *
 * @param {string} code - The CNS11643 code to be converted.
 * @return {number} - The corresponding order of the CNS11643 code.
 */
export function cns11643ToOrder (code) {
  if (code === '') {
    return -1
  }
  const [plane, codePoint] = code.split('-')
  const offset = plane === '1' ? 0 : 5546
  const hiStart = plane === '1' ? '44' : '21'
  const hi = parseInt(codePoint.slice(0, 2), 16) - parseInt(hiStart, 16)
  const lo = parseInt(codePoint.slice(2), 16) - parseInt('21', 16)
  return offset + hi * 94 + lo
}

/**
 * Converts a given order value to a corresponding CNS11643 character.
 *
 * @param {number} order - The order value to be converted.
 * @return {string} - The CNS11643 character corresponding to the given order value.
 */
export function orderToCNS11643 (order) {
  if (order < 0) {
    return ''
  }
  if (order < 5401) {
    const hi = Math.floor(order / 94)
    const lo = order % 94
    return `${1}-${((hi + 0x44) << 8) | (lo + 0x21)}`
  }
  order -= 5546 // 5401 + 145 (MAGIC NUM)
  const hi = Math.floor(order / 94)
  const lo = order % 94
  return `${2}-${((hi + 0x21) << 8) | (lo + 0x21)}`
}

export function unicodeToCNS11643 (code) {
  if (code in unicodeToCNS11643OrderTable) {
    return unicodeToCNS11643OrderTable[code][0]
  }
  return ''
}

export function cns11643ToUnicode (code) {
  if (code in cns11643ToUnicodeTable) {
    return cns11643ToUnicodeTable[code]
  }
  return ''
}

export function orderOfUnicode (code) {
  if (code in unicodeToCNS11643OrderTable) {
    return unicodeToCNS11643OrderTable[code][1]
  }
  return -1
}

export function orderToUnicode (order) {
  if (order < 0 || order >= orderToUnicodeTable.length) {
    return ''
  }
  return orderToUnicodeTable[order]
}
