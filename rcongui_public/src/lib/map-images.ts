import { MapLayer } from '@/types/mapLayer'

const MAP_IMAGE_ALIASES: Record<string, string> = {
  phll1944: 'purpleheartlane',
  phll: 'purpleheartlane',
  phl: 'purpleheartlane',
  hurtgenforestv2: 'hurtgenforest',
}

function normalizeKey(value: string | undefined | null): string {
  return (value ?? '').toLowerCase().replace(/[^a-z0-9]/g, '')
}

function getCanonicalMapId(map: MapLayer): string {
  const candidates = [
    map.map.id,
    map.map.pretty_name,
    map.map.shortname,
    map.map.tag,
    map.id,
    map.pretty_name,
  ]

  for (const candidate of candidates) {
    const normalized = normalizeKey(candidate)
    if (!normalized) {
      continue
    }
    if (MAP_IMAGE_ALIASES[normalized]) {
      return MAP_IMAGE_ALIASES[normalized]
    }
    return normalized
  }

  return 'unknown'
}

export function getMapImageName(map: MapLayer): string {
  return `${getCanonicalMapId(map)}-${map.environment}.webp`
}