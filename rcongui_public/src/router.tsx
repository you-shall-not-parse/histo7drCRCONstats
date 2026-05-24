import { createBrowserRouter, Navigate, RouteObject } from 'react-router'
import ErrorPage from './components/error-page'
import Layout from './components/layout'
import GamesLayout from './pages/games/layout'
import GamesList from './pages/games'
import GameDetail from './pages/games/[id]'
import GameDetailLayout from './pages/games/[id]/layout'
import GameDetailCharts from './pages/games/[id]/charts'
import { queryClient } from './lib/queryClient'
import { clientLoader as layoutClientLoader } from './components/layout/clientLoader'
import { clientLoader as gameClientLoader } from './pages/games/clientLoader'
import { clientLoader as gameDetailClientLoader } from './pages/games/[id]/clientLoader'

function getLegacyGameTarget(path: string, search = '') {
  const normalizedPath = path.replace(/\/$/, '') || '/'
  const match = normalizedPath.match(/^\/(?:stats\/)?gamescoreboard(?:\/(\d+)(\/charts)?)?$/)

  if (match) {
    const [, gameId, chartsSuffix] = match
    if (gameId) {
      return chartsSuffix ? `/games/${gameId}/charts` : `/games/${gameId}`
    }

    const params = new URLSearchParams(search)
    const queryGameId = params.get('map_id') ?? params.get('gameId') ?? params.get('id')
    return queryGameId ? `/games/${queryGameId}` : '/games'
  }

  const statsMatch = normalizedPath.match(/^\/stats\/games(?:\/(\d+)(\/charts)?)?$/)
  if (!statsMatch) {
    return null
  }

  const [, gameId, chartsSuffix] = statsMatch
  if (gameId) {
    return chartsSuffix ? `/games/${gameId}/charts` : `/games/${gameId}`
  }

  return '/games'
}

function normalizeLegacyGameLocation() {
  if (typeof window === 'undefined') {
    return
  }

  const hashPath = window.location.hash.startsWith('#') ? window.location.hash.slice(1) : ''
  const [hashRoutePath, hashRouteSearch = ''] = hashPath.split('?')
  const hashTarget = hashPath
    ? getLegacyGameTarget(hashRoutePath, hashRouteSearch ? `?${hashRouteSearch}` : '')
    : null
  const pathTarget = getLegacyGameTarget(window.location.pathname, window.location.search)
  const target = hashTarget ?? pathTarget

  if (!target) {
    return
  }

  const currentPath = `${window.location.pathname}${window.location.search}`
  if (target !== currentPath) {
    window.history.replaceState(null, '', target)
  }
}

normalizeLegacyGameLocation()

export const routerObjects: RouteObject[] = [
  {
    path: '/',
    element: <Layout />,
    errorElement: <ErrorPage />,
    loader: layoutClientLoader(queryClient),
    children: [
      {
        index: true,
        element: <Navigate to="/games" replace />,
      },
      {
        path: '/streaming',
        element: <Navigate to="/games" replace />,
      },
      {
        path: '/games',
        element: <GamesLayout />,
        errorElement: <ErrorPage />,
        loader: gameClientLoader(queryClient),
        children: [
          {
            index: true,
            element: <GamesList />,
            loader: gameClientLoader(queryClient),
          },
          {
            path: ':id/*',
            element: <GameDetailLayout />,
            loader: gameDetailClientLoader(queryClient),
            children: [
              {
                index: true,
                element: <GameDetail />,
              },
              {
                path: 'charts',
                element: <GameDetailCharts />,
              },
            ],
          },
        ],
      },
      {
        path: '/gamescoreboard',
        element: <GamesLayout />,
        errorElement: <ErrorPage />,
        loader: gameClientLoader(queryClient),
        children: [
          {
            index: true,
            element: <GamesList />,
            loader: gameClientLoader(queryClient),
          },
          {
            path: ':id/*',
            element: <GameDetailLayout />,
            loader: gameDetailClientLoader(queryClient),
            children: [
              {
                index: true,
                element: <GameDetail />,
              },
              {
                path: 'charts',
                element: <GameDetailCharts />,
              },
            ],
          },
        ],
      },
      {
        path: '/stats/games',
        element: <GamesLayout />,
        errorElement: <ErrorPage />,
        loader: gameClientLoader(queryClient),
        children: [
          {
            index: true,
            element: <GamesList />,
            loader: gameClientLoader(queryClient),
          },
          {
            path: ':id/*',
            element: <GameDetailLayout />,
            loader: gameDetailClientLoader(queryClient),
            children: [
              {
                index: true,
                element: <GameDetail />,
              },
              {
                path: 'charts',
                element: <GameDetailCharts />,
              },
            ],
          },
        ],
      },
    ],
  },
]

export function createRouter(): ReturnType<typeof createBrowserRouter> {
  return createBrowserRouter(routerObjects)
}
