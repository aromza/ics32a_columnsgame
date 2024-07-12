# project5.py

import pygame
# Import game rules. 

BACKGROUND_COLOR = pygame.Color (100, 100, 100)
COLUMN_NUM = 6
ROW_NUM = 13

class ColumnsGame:
    def __init__ (self):
        self._running = True

    def run (self) -> None:
        pygame.init ()
        try:
            self._surface = pygame.display.set_mode ((800, 600))
            
            clock = pygame.time.Clock () 

            while self._running:
                clock.tick (30)
                self._handle_events ()
                self._redraw () 
        finally: 
            pygame.quit ()


    def _handle_events (self) -> None:
        for event in pygame.event.get ()
            self._handle_event (event)

    def _handle_event (self, event) -> None:
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pass
            elif event.key == pygame.K_RIGHT:
                pass

    def _redraw (self) -> None:
        self._surface.fill (BACKGROUND_COLOR)
        pygame.display.flip ()

if __name__ == '__main__':
    ColumnsGame().run() 
        
