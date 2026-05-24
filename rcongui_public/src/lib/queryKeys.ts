export const queryKeys = {
  publicInfo: ['public-info'],
  games: (page: number, pageSize: number) => ['games', page, pageSize],
  gameDetail: (gameId: number) => ['game', gameId],
}
