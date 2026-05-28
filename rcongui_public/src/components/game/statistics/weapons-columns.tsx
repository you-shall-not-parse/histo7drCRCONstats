'use client'

import { ColumnDef } from '@tanstack/react-table'
import { Header } from './column-header'
import { useTranslation } from 'react-i18next'

const nColSize = 40

type WeaponKillCount = {
  name: string
  count: number
}

export const useKillByColumns = (): ColumnDef<WeaponKillCount>[] => {
  const { t } = useTranslation('game')

  return [
    {
      accessorKey: 'name',
      header: () => t('playerStats.weapon'),
    },
    {
      accessorKey: 'count',
      header: function KillsHeader({ column }) {
        return (
          <Header
            header={'K'}
            desc={t('playersTable.kills')}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
      cell: ({ cell }) => <div className="text-center px-1">{String(cell.getValue())}</div>,
      size: nColSize,
    },
  ]
}

export const useDeathByColumns = (): ColumnDef<WeaponKillCount>[] => {
  const { t } = useTranslation('game')

  return [
    {
      accessorKey: 'name',
      header: () => t('playerStats.weapon'),
    },
    {
      accessorKey: 'count',
      header: function DeathsHeader({ column }) {
        return (
          <Header
            header={'D'}
            desc={t('playersTable.deaths')}
            onClick={() => {
              column.toggleSorting(column.getIsSorted() !== 'desc')
            }}
          />
        )
      },
      cell: ({ cell }) => <div className="text-center px-1">{String(cell.getValue())}</div>,
      size: nColSize,
    },
  ]
}
