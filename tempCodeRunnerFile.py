bacteriaAntidoteCollision = pygame.sprite.spritecollide(player, all_sprites_list, True)
            
            if bacteriaAntidoteCollision == True:
                antidoteCollide = bacteriaAntidoteCollision[0]
                if antidoteCollide.size > bacteriaSize[0]:
                    gameover = True
                else:
                    continue