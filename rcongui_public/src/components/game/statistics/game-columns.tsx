'use client'

import {Column, ColumnDef} from '@tanstack/react-table'
import {Player, PlayerTeamAssociation, PlayerWithStatus} from '@/types/player'
import {IconHeader as Header} from './column-header'
import {Status} from './player-status'
import {isPlayerWithStatus} from './player/utils'
import {Button} from '@/components/ui/button'
import {useTranslation} from 'react-i18next'
import {TeamIndicator} from '@/components/game/statistics/team-indicator'
import {WeaponTypeBar} from "@/components/game/statistics/weapon-type-bar";
import {getTeamFromAssociation} from "@/components/game/statistics/utils";
import {HeartCrackIcon, HeartOffIcon, ScaleIcon, SkullIcon, ZapIcon} from "lucide-react";
import {ColumnCategory} from "@/lib/tables";
import {Awards} from "@/components/game/statistics/award";
import {PlayerBaseWithAwards} from "@/pages/games/[id]";
import { Level } from './level'
import { TFunction } from 'i18next'

const threeDigitsWidth = 40
const fourDigitsWidth = 50

function SortableHeader({ column, desc }: { column: Column<Player>; desc: string }) {
  return (
    <div className="text-right">
      <Button
        variant={'text'}
        onClick={() => {
          column.toggleSorting(column.getIsSorted() !== 'desc')
        }}
        className="px-0"
      >
        {desc}
      </Button>
    </div>
  )
}

function pointColumns(t: TFunction, completed: boolean): ColumnDef<Player | PlayerWithStatus>[] {
  return [
    ...(completed ? [killCategoryColumn(t)] : []),
    {
      id: 'kills',
      meta: { label: t('playersTable.kills'), category: ColumnCategory.GENERAL },
      accessorKey: 'kills',
      size: threeDigitsWidth,
      header: function KillsHeader({ column }) {
        return (
          <Header
            src={'/icons/roles/infantry.png'}
            desc={t('playersTable.kills')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
    },
    {
      id: 'kill_death_ratio',
      meta: { label: t('score.k/d'), category: ColumnCategory.GENERAL },
      accessorKey: 'kill_death_ratio',
      size: fourDigitsWidth,
      header: function KDHeader({ column }) {
        return (
          <Header
            icon={<ScaleIcon/>}
            desc={t('score.k/d')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
      cell: ({row}) => {
        const player = row.original;
        return <div className={"text-right whitespace-pre"}>
          {player.kill_death_ratio.toFixed(1)}
        </div>;
      },
    },
    {
      id: 'deaths',
      meta: { label: t('playersTable.deaths'), category: ColumnCategory.GENERAL },
      accessorKey: 'deaths',
      size: fourDigitsWidth,
      header: function DeathsHeader({ column }) {
        return (
          <Header
            src={'/icons/roles/medic.png'}
            desc={t('playersTable.deaths')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
    },
    ...(completed ? [deathCategoryColumn(t)] : []),
    {
      id: 'kills_per_minute',
      meta: { label: t('playersTable.killsPerMinute'), category: ColumnCategory.ADVANCED},
      accessorKey: 'kills_per_minute',
      header: function KpmHeader({ column }) {
        return <SortableHeader column={column} desc={t('playersTable.killsPerMinute')} />
      },
      size: 20,
    },
    {
      id: 'deaths_per_minute',
      meta: { label: t('playersTable.deathsPerMinute'), category: ColumnCategory.ADVANCED },
      accessorKey: 'deaths_per_minute',
      header: function KpmHeader({ column }) {
        return <SortableHeader column={column} desc={t('playersTable.deathsPerMinute')} />
      },
      size: 20,
    },
    {
      id: 'kills_streak',
      meta: { label: t('score.killstreak'), category: ColumnCategory.ADVANCED },
      accessorKey: 'kills_streak',
      header: function KillStreakHeader({ column }) {
        return (
          <Header
            icon={<ZapIcon/>}
            desc={t('score.killstreak')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
      size: 20,
    },
    {
      id: 'deaths_without_kill_streak',
      meta: { label: t('score.deathstreak'), category: ColumnCategory.ADVANCED },
      accessorKey: 'deaths_without_kill_streak',
      header: function DeathStreakHeader({ column }) {
        return (
          <Header
            icon={<SkullIcon/>}
            desc={t('score.deathstreak')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
      size: 20,
    },
    {
      id: 'teamkills',
      meta: { label: t('score.teamkills'), category: ColumnCategory.ADVANCED },
      accessorKey: 'teamkills',
      header: function TeamkillsHeader({ column }) {
        return (
          <Header
            icon={<HeartOffIcon/>}
            desc={t('score.teamkills')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
      size: 20,
    },
    {
      id: 'deaths_by_tk',
      meta: { label: t('score.deathsByTeam'), category: ColumnCategory.ADVANCED },
      accessorKey: 'deaths_by_tk',
      header: function DeathsByTkHeader({ column }) {
        return (
          <Header
            icon={<HeartCrackIcon/>}
            desc={t('score.deathsByTeam')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
      size: 20,
    },
    {
      id: 'combat',
      meta: { label: t('playersTable.combat'), category: ColumnCategory.INGAME},
      accessorKey: 'combat',
      size: fourDigitsWidth,
      header: function CombatHeader({ column }) {
        return (
          <Header
            src={'/icons/roles/score_combat.png'}
            desc={t('playersTable.combat')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
    },
    {
      id: 'offense',
      meta: { label: t('playersTable.offense'), category: ColumnCategory.INGAME },
      accessorKey: 'offense',
      size: fourDigitsWidth,
      header: function OffenseHeader({ column }) {
        return (
          <Header
            src={'/icons/roles/score_offensive.png'}
            desc={t('playersTable.offense')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
    },
    {
      id: 'defense',
      meta: { label: t('playersTable.defense'), category: ColumnCategory.INGAME },
      accessorKey: 'defense',
      size: fourDigitsWidth,
      header: function DefenseHeader({ column }) {
        return (
          <Header
            src={'/icons/roles/score_defensive.png'}
            desc={t('playersTable.defense')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
    },
    {
      id: 'support',
      meta: { label: t('playersTable.support'), category: ColumnCategory.INGAME },
      accessorKey: 'support',
      size: fourDigitsWidth,
      header: function SupportHeader({ column }) {
        return (
          <Header
            src={'/icons/roles/score_support.png'}
            desc={t('playersTable.support')}
            className={"text-right"}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
    },
  ]
}

const playerColumn = (t: TFunction, handlePlayerClick: (id: string) => void): ColumnDef<Player | PlayerWithStatus> => ({
  id: 'player',
  accessorKey: 'player',
  header: function NameHeader({ column }) {
    return (
      <div className="text-left">
        <Button
          variant={'text'}
          onClick={() => {
            column.toggleSorting(column.getIsSorted() === 'asc')
          }}
          className="px-0"
        >
          {t('playersTable.player')}
        </Button>
      </div>
    )
  },
  cell: ({ row }) => {
    const name = String(row.getValue('player'))
    const id = String(row.original.player_id)

    return (
      <div className="text-left">
        <Button
          variant={'text'}
          className="pl-0"
          onClick={() => {
            handlePlayerClick(id)
          }}
        >
          {name}
        </Button>
      </div>
    )
  },
  filterFn: (row, columnId: string, filterValue: string[]) => {
    if (filterValue === undefined || filterValue.length === 0) {
      return true
    }
    const value: string = row.getValue(columnId)
    return filterValue.some((v: string) => value.toLowerCase().includes(v.toLowerCase()))
  },
  enableHiding: false,
})

const awardColumn = (t: TFunction): ColumnDef<Player | PlayerBaseWithAwards | PlayerWithStatus>  => {
  return {
    id: 'award',
    meta: {label: t('playersTable.awards'), category: ColumnCategory.GENERAL},
    header: function NameHeader() {
      return <div className="text-right">{t('playersTable.awards')}</div>
    },
    cell: ({row}) => {
      return 'awards' in row.original ? <Awards player={row.original}/> : null
    },
    size: 20,
  }
};

const teamColumn = (t: TFunction): ColumnDef<Player | PlayerWithStatus> => {
  return {
    id: 'team',
    meta: { label: t('playersTable.team'), category: ColumnCategory.GENERAL },
    accessorKey: 'team',
    header: function TeamHeader() {
      return <div className={"text-center"}>{t('playersTable.team')}</div>
    },
    size: 20,
    filterFn: (row, columnId, filterValue) => {
      if (!filterValue || filterValue === 'all') {
        return true
      }
      const cellValue: PlayerTeamAssociation = row.getValue(columnId);
      return getTeamFromAssociation(cellValue) === filterValue;
    },
    cell: ({row}) => {
      const player = row.original;
      return <div className={"text-center"}>
        <TeamIndicator team={getTeamFromAssociation(player.team)}/>
      </div>;
    },
  }
}

const killCategoryColumn = (t: TFunction): ColumnDef<Player | PlayerWithStatus> => {
  return {
    id: 'kills_by_category',
    meta: { label: t('playersTable.killsByCategory'), category: ColumnCategory.GENERAL },
    accessorKey: 'kills_by_category',
    header: function KillCategoryHeader() {
      return <div>{t('playersTable.killsByCategory')}</div>
    },
    size: 125,
    cell: ({row}) => {
      const player = row.original;
      return <WeaponTypeBar totalKills={player.kills} killsByType={player.kills_by_type}/>;
    },
  }
};

const deathCategoryColumn = (t: TFunction): ColumnDef<Player | PlayerWithStatus> => {
  return {
    id: 'deaths_by_category',
    meta: { label: t('playersTable.deathsByCategory'), category: ColumnCategory.GENERAL },
    accessorKey: 'deaths_by_category',
    header: function DeathCategoryHeader() {
      return <div>{t('playersTable.deathsByCategory')}</div>
    },
    size: 125,
    cell: ({row}) => {
      const player = row.original;
      return <WeaponTypeBar totalKills={player.deaths} killsByType={player.deaths_by_type}/>;
    },
  }
};

const statusColumn = (t: TFunction): ColumnDef<Player | PlayerWithStatus> => ({
  id: 'is_online',
  accessorKey: 'is_online',
  header: function StatusHeader() {
    return <div className="sr-only w-4">{t('playersTable.status')}</div>
  },
  size: 20,
  filterFn: (row, columnId, filterValue) => {
    if (!filterValue || filterValue === 'all') {
      return true
    }
    const cellValue = row.getValue(columnId) ? 'online' : 'offline'
    return cellValue === filterValue
  },
  cell: ({ row }) => {
    const player = row.original
    return isPlayerWithStatus(player) ? <Status player={player} className="block" /> : null
  },
  enableHiding: false,
})

const levelColumn = (t: TFunction): ColumnDef<Player | PlayerWithStatus> => {
  return {
    id: 'level',
    accessorKey: 'level',
    meta: { label: t('playersTable.level'), category: ColumnCategory.GENERAL },
    size: threeDigitsWidth,
    header: function LevelHeader() {
      return <div>{t('playersTable.level')}</div>
    },
    cell: ({ row }) => {
      const player = row.original
      return <div className='text-center font-bold'><Level level={player.level} /></div>
    },
  }
}

export const useLiveGameColumns = (handlePlayerClick: (id: string) => void): ColumnDef<Player | PlayerWithStatus>[] => {
  const { t } = useTranslation('game')

  return [
    statusColumn(t),
    levelColumn(t),
    playerColumn(t, handlePlayerClick),
    ...pointColumns(t, false),
  ]
}

export const useCompletedGameColumns = (
  handlePlayerClick: (id: string) => void,
): ColumnDef<Player | PlayerWithStatus | PlayerBaseWithAwards>[] => {
  const { t } = useTranslation('game')

  return [
    teamColumn(t),
    levelColumn(t),
    playerColumn(t, handlePlayerClick),
    awardColumn(t),
    ...pointColumns(t, true),
  ]
}
