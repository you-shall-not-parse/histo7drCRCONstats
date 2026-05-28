'use client'

import {ColumnDef} from '@tanstack/react-table'
import dayjs from 'dayjs'
import LocalizedFormat from 'dayjs/plugin/localizedFormat'
import {Button} from '@/components/ui/button'
import {Link} from 'react-router'
import {getGameDuration} from './utils'
import {ScoreboardMap} from '@/types/api'
import {MapLayer} from '@/types/mapLayer'
import {useTranslation} from 'react-i18next'
import {dayjsLocal} from "@/lib/utils";
import WeatherIcon from "@/components/game/weather-icon";
import { Badge } from '@/components/ui/badge'

dayjs.extend(LocalizedFormat)

function fallbackMapImage(event: React.SyntheticEvent<HTMLImageElement>, fallbackBasePath: string) {
  const image = event.currentTarget
  const fallbackStep = image.dataset.fallbackStep ?? '0'
  const mapId = image.dataset.mapId ?? 'unknown'

  if (fallbackStep === '0') {
    image.dataset.fallbackStep = '1'
    image.src = `${fallbackBasePath}/${mapId}-day.webp`
    return
  }

  if (fallbackStep === '1') {
    image.dataset.fallbackStep = '2'
    image.src = `${fallbackBasePath}/unknown-day.webp`
  }
}

export function useGameColumns(): ColumnDef<ScoreboardMap>[] {
  const { t } = useTranslation('game')
  const { t: translationT } = useTranslation('translation')

  return [
    {
      accessorKey: 'id',
      header: 'ID',
      cell: ({ cell }) => {
        const gameId = cell.getValue() as string
        return (
          <Button asChild variant={'link'}>
            <Link to={`/games/${gameId}`} className="w-10">
              {gameId}
            </Link>
          </Button>
        )
      },
    },
    {
      header: t('matchTable.map'),
      id: 'map',
      accessorKey: 'map',
      cell: function MapCell({ cell }) {
        const gameMap = cell.getValue() as MapLayer
        const size = 60
        const ratio = 9 / 16

        return (
          <div className="flex flex-row items-center gap-2 w-max">
            <img
              src={'/maps/icons/' + gameMap.image_name}
              width={size}
              height={size * ratio}
              alt=""
              data-map-id={gameMap.map.id}
              data-fallback-step="0"
              onError={(event) => fallbackMapImage(event, '/maps/icons')}
            />
            <span>{gameMap.map.pretty_name}</span>
          </div>
        )
      },
    },
    {
      header: t('matchTable.weather'),
      id: 'weather',
      accessorKey: 'map',
      cell: function MapCell({ cell }) {
        const gameMap = cell.getValue() as MapLayer

        return (
          <WeatherIcon environment={gameMap.environment} className="text-muted-foreground"/>
        )
      },
    },
    {
      header: t('matchTable.mode'),
      id: 'mode',
      accessorKey: 'map',
      cell: function MapCell({cell}) {
        const gameMap = cell.getValue() as MapLayer

        return (
          <div>
            <span>{gameMap.game_mode[0].toUpperCase() + gameMap.game_mode.slice(1)}</span>
            {gameMap.attackers &&
              <span> ({gameMap.map[gameMap.attackers].name.toUpperCase()})</span>
            }
          </div>
        )
      },
    },
    {
      header: t('matchTable.result'),
      id: 'result',
      accessorFn: (row) => `${row.result?.allied ?? '?'} - ${row.result?.axis ?? '?'}`,
    },
    {
      header: 'Clans',
      id: 'clan_match',
      accessorKey: 'clan_match',
      cell: ({ row }) => {
        const clans = row.original.clan_match?.clans ?? []

        if (clans.length === 0) {
          return <span className="text-muted-foreground">-</span>
        }

        return (
          <div className="flex flex-wrap gap-1 max-w-48">
            {clans.map((clan) => (
              <Badge key={clan.tag} variant={row.original.clan_match.detected ? 'default' : 'secondary'}>
                {clan.tag} {clan.count}
              </Badge>
            ))}
          </div>
        )
      },
    },
    {
      header: translationT('time.weekday'),
      id: 'weekday',
      accessorKey: 'start',
      cell: ({ cell }) => {
        const globalLocaleData = dayjs.localeData();
        return globalLocaleData.weekdaysShort()[dayjsLocal(cell.getValue() as string).day()];
      },
    },
    {
      header: t('matchTable.start'),
      id: 'start',
      accessorKey: 'start',
      cell: ({ cell }) => dayjsLocal(cell.getValue() as string).format('L LT'),
    },
    {
      header: t('matchTable.duration'),
      id: 'duration',
      accessorKey: 'duration',
      cell: ({ row }) => getGameDuration(row.original.start, row.original.end),
    },
  ]
}
