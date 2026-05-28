import { cn } from '@/lib/utils'
import React, { ReactNode } from 'react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { ScoreboardMap } from "@/types/api";

type MapFigureProps = {
  src: string
  name: string
  text?: string
  muted?: boolean
  gameLayout?: ScoreboardMap['game_layout']
} & React.ComponentProps<'figure'>

function fallbackFigureImage(event: React.SyntheticEvent<HTMLImageElement>) {
  const image = event.currentTarget
  const fallbackStep = image.dataset.fallbackStep ?? '0'
  const source = image.getAttribute('src') ?? ''
  const pathPrefix = source.includes('/maps/icons/') ? '/maps/icons' : '/maps'
  const currentFile = source.split('/').pop() ?? 'unknown-day.webp'
  const mapId = currentFile.replace(/-(day|night|dawn|dusk|rain|overcast)\.webp$/i, '') || 'unknown'

  if (fallbackStep === '0') {
    image.dataset.fallbackStep = '1'
    image.src = `${pathPrefix}/${mapId}-day.webp`
    return
  }

  if (fallbackStep === '1') {
    image.dataset.fallbackStep = '2'
    image.src = `${pathPrefix}/unknown-day.webp`
  }
}

export default function MapFigure({ gameLayout, src, name, text, muted, ...props }: MapFigureProps) {
  let caps = (content: ReactNode) => content;
  if (gameLayout && gameLayout?.set?.length || 0 > 0) {
    caps = (content: ReactNode) => (
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>{content}</TooltipTrigger>
          <TooltipContent>
            <span>{gameLayout?.set?.join(', ')}</span>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    )
  }
  return (
    <figure className={cn('relative min-h-12', props.className)}>
      <img
        src={src}
        alt=""
        data-fallback-step="0"
        onError={fallbackFigureImage}
        className={cn('w-full h-full object-cover', muted ? 'grayscale-[50]' : '')}
      />
      <figcaption className="absolute bottom-0 min-h-12 w-full p-1 text-center text-sm font-bold bg-background/75 group-hover:bg-background/60">
        {text && <div className="text-xs">{text}</div>}
        {caps(<div>{name}</div>)}
      </figcaption>
    </figure>
  )
}
