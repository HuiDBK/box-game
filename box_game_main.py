# -*- Coding:UTF-8 -*-
"""
推箱子游戏主模块
author:Mr Liu
version:1.0
"""

import os
import sys
import pyautogui as gui
from game_sprites import *

pygame.init()

# 获取电脑屏幕分辨率
screen_width, screen_height = gui.size()
game_x = (screen_width - SCREEN_RECT.width) / 2
game_y = (screen_height - SCREEN_RECT.height) / 2
# 设置游戏窗口相对电脑屏幕居中
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_x, game_y)

game_maps = {
    1: [
        [9, 9, 1, 1, 1, 9, 9, 9],
        [9, 9, 1, 4, 1, 9, 9, 9],
        [9, 9, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 2, 0, 2, 4, 1],
        [1, 4, 0, 2, 3, 1, 1, 1],
        [1, 1, 1, 1, 2, 1, 9, 9],
        [9, 9, 9, 1, 4, 1, 9, 9],
        [9, 9, 9, 1, 1, 1, 9, 9]
    ],
    2: [
        [9, 9, 1, 1, 1, 1, 9, 9],
        [9, 9, 1, 4, 4, 1, 9, 9],
        [9, 1, 1, 0, 4, 1, 1, 9],
        [9, 1, 0, 0, 2, 4, 1, 9],
        [1, 1, 0, 2, 3, 0, 1, 1],
        [1, 0, 0, 1, 2, 2, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ],
    3: [
        [9, 9, 1, 1, 1, 1, 9, 9],
        [9, 1, 1, 0, 0, 1, 9, 9],
        [9, 1, 3, 2, 0, 1, 9, 9],
        [9, 1, 1, 2, 0, 1, 1, 9],
        [9, 1, 1, 0, 2, 0, 1, 9],
        [9, 1, 4, 2, 0, 0, 1, 9],
        [9, 1, 4, 4, 6, 4, 1, 9],
        [9, 1, 1, 1, 1, 1, 1, 9]
    ],
    4: [
        [1, 1, 1, 1, 1, 9, 9, 9, 9],
        [1, 0, 0, 0, 1, 1, 1, 1, 1],
        [1, 2, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 3, 0, 0, 2, 0, 1],
        [1, 4, 5, 1, 2, 1, 2, 1, 1],
        [1, 4, 2, 0, 0, 0, 0, 1, 9],
        [1, 4, 4, 0, 0, 1, 1, 1, 9],
        [1, 1, 1, 1, 1, 1, 9, 9, 9]
    ],
    5: [
        [9, 1, 1, 1, 1, 1, 1, 9],
        [9, 1, 0, 0, 0, 0, 1, 9],
        [9, 1, 0, 2, 2, 0, 1, 9],
        [9, 1, 1, 6, 3, 0, 1, 9],
        [9, 1, 0, 4, 0, 1, 9, 9],
        [9, 1, 0, 6, 0, 1, 9, 9],
        [9, 1, 0, 6, 0, 1, 9, 9],
        [9, 1, 0, 4, 0, 1, 9, 9],
        [9, 1, 1, 1, 1, 1, 9, 9]
    ],

    6: [
        [9, 1, 1, 1, 1, 1, 1, 9, 9],
        [9, 1, 0, 0, 0, 0, 1, 1, 9],
        [1, 1, 4, 1, 1, 3, 0, 1, 9],
        [1, 0, 6, 5, 0, 0, 0, 1, 9],
        [1, 0, 0, 1, 2, 2, 0, 1, 9],
        [1, 0, 0, 0, 0, 1, 1, 1, 9],
        [1, 1, 1, 1, 1, 1, 9, 9, 9],
        [9, 9, 9, 9, 9, 9, 9, 9, 9]

    ],
    7: [
        [9, 1, 1, 1, 1, 1, 9, 9, 9],
        [9, 1, 0, 3, 0, 1, 1, 1, 9],
        [1, 1, 0, 1, 2, 0, 0, 1, 9],
        [1, 0, 6, 4, 0, 4, 0, 1, 9],
        [1, 0, 0, 2, 2, 0, 1, 1, 9],
        [1, 1, 1, 0, 1, 4, 1, 9, 9],
        [9, 9, 1, 0, 0, 0, 1, 9, 9],
        [9, 9, 1, 1, 1, 1, 1, 9, 9]

    ],
    8: [
        [1, 1, 1, 1, 1, 1, 1, 9],
        [1, 4, 4, 2, 4, 4, 1, 9],
        [1, 4, 4, 1, 4, 4, 1, 9],
        [1, 0, 2, 2, 2, 0, 1, 9],
        [1, 0, 0, 2, 0, 0, 1, 9],
        [1, 0, 2, 2, 2, 0, 1, 9],
        [1, 0, 0, 1, 3, 0, 1, 9],
        [1, 1, 1, 1, 1, 1, 1, 9]

    ],
    9: [
        [1, 1, 1, 1, 1, 1, 9, 9],
        [1, 0, 0, 0, 0, 1, 9, 9],
        [1, 0, 4, 6, 0, 1, 1, 1],
        [1, 0, 4, 2, 4, 2, 0, 1],
        [1, 1, 0, 2, 0, 0, 0, 1],
        [9, 1, 1, 1, 1, 0, 3, 1],
        [9, 9, 9, 9, 1, 1, 1, 1],
        [9, 9, 9, 9, 9, 9, 9, 9]
    ],
    10: [
        [9, 9, 1, 1, 1, 1, 1, 9, 9],
        [9, 1, 1, 0, 3, 0, 1, 1, 9],
        [9, 1, 0, 0, 6, 2, 0, 1, 9],
        [9, 1, 2, 0, 4, 0, 2, 1, 9],
        [9, 1, 4, 4, 1, 4, 4, 1, 9],
        [1, 1, 2, 0, 6, 0, 0, 1, 1],
        [1, 0, 2, 0, 1, 0, 2, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
}


class BoxGame(object):
    """推箱子游戏主类"""

    def __init__(self, game_level=1):
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.game_name = pygame.display.set_caption(GAME_NAME)
        self.game_clock = pygame.time.Clock()
        # 默认游戏关卡为1
        self.game_level = game_level
        self.game_map = game_maps[self.game_level]
        self.is_first = True
        # 记录游戏角色移动方向
        self.move_direction = None
        # 初始化游戏地图
        self.__init_game_map()
        self.__create_sprite()

    def start_game(self):
        """游戏开始"""
        while True:
            self.game_clock.tick(FRAME_PRE_SEC)
            self.__event_handle()
            self.__check_collision()
            self.__update_sprite()
            self.__update_game_level()
            pygame.display.update()
            pass

    def __event_handle(self):
        """游戏事件监听"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # print(pygame.key.name(event.key))
                self.__move_event(event)
            elif event.type == pygame.KEYUP:
                print("keyup")
        pass

    def __create_sprite(self):

        # 创建游戏背景
        game_bg_sprite = GameSprite(GAME_BACKGROUND, self.game_map)
        self.game_bg_group = pygame.sprite.Group(game_bg_sprite)

        # 创建游戏角色
        self.game_person_sprite = GamePerson(PERSON_IMAGE, self.game_map)
        self.game_person_group = pygame.sprite.Group(self.game_person_sprite)

        # 创建游戏箱子
        self.box_group = pygame.sprite.Group()
        for box_count in range(self.box_counts):
            box_sprite = Box(BOX_IMAGE, self.game_map)
            box_sprite.set_sprite_pos(box_count, BOX_FLAG)
            self.box_group.add(box_sprite)

        # 创建游戏墙
        self.wall_group = pygame.sprite.Group()
        for wall_count in range(self.wall_counts):
            wall_sprite = GameSprite(GAME_WALL, self.game_map)
            wall_sprite.set_sprite_pos(wall_count, WALL_FLAG)
            self.wall_group.add(wall_sprite)

        # 创建游戏箱子目的地
        self.box_terminal_group = pygame.sprite.Group()
        for terminal_count in range(self.terminal_counts):
            box_terminal_sprite = GameSprite(TERMINAL_IMAGE, self.game_map)
            box_terminal_sprite.set_sprite_pos(terminal_count, TERMINAL_FLAG)
            self.box_terminal_group.add(box_terminal_sprite)

    def __update_sprite(self):
        """更新精灵"""
        self.game_bg_group.update()
        self.game_bg_group.draw(self.screen)

        self.game_person_group.update()
        self.game_person_group.draw(self.screen)

        self.box_group.update()
        self.box_group.draw(self.screen)

        self.wall_group.update()
        self.wall_group.draw(self.screen)

        self.box_terminal_group.update()
        self.box_terminal_group.draw(self.screen)

    def __check_collision(self):
        """检查精灵之间的碰撞"""

        # 游戏角色与游戏箱子发生碰撞，根据移动的方向改变箱子的位置
        box_sprite = pygame.sprite.spritecollide(self.game_person_sprite, self.box_group, False)
        if box_sprite:
            if self.move_direction is not None:
                if self.move_direction == "up":
                    box_sprite[0].rect.y = box_sprite[0].rect.y - box_sprite[0].rect.height
                    self.__box_wall_box_collide(box_sprite)
                elif self.move_direction == "down":
                    box_sprite[0].rect.y = box_sprite[0].rect.y + box_sprite[0].rect.height
                    self.__box_wall_box_collide(box_sprite)
                elif self.move_direction == "left":
                    box_sprite[0].rect.x = box_sprite[0].rect.x - box_sprite[0].rect.width
                    self.__box_wall_box_collide(box_sprite)
                elif self.move_direction == "right":
                    box_sprite[0].rect.x = box_sprite[0].rect.x + box_sprite[0].rect.width
                    self.__box_wall_box_collide(box_sprite)

        # 游戏箱子与箱子的目的地发生碰撞,目的地图片更换成星星
        result = pygame.sprite.groupcollide(self.box_group, self.box_terminal_group, False, False)
        if result:
            for box_sprite, terminal_sprite in result.items():
                terminal_sprite[0].image = pygame.image.load(STAR_IMAGE)
                terminal_sprite[0].is_success = True

        # 游戏角色与墙发生碰撞,游戏角色移动方向的相反方向回退保持原位不动
        wall_sprite = pygame.sprite.spritecollide(self.game_person_sprite, self.wall_group, False)
        if wall_sprite:
            self.__back_person()

        # 游戏角色与目的地发生碰撞，目的地更换图片为t_man.png
        terminal_sprite = pygame.sprite.spritecollide(self.game_person_sprite, self.box_terminal_group, False)
        if terminal_sprite:
            # 把没有变成星星的图片还原,然后在更换
            for t_sprite in self.box_terminal_group.sprites():
                if not t_sprite.is_success:
                    t_sprite.image = pygame.image.load(TERMINAL_IMAGE)
            terminal_sprite[0].image = pygame.image.load(TERMINAL_PERSON_IMAGE)
            terminal_sprite[0].is_success = False
        else:
            # 没有发生碰撞时记得把没有变成星星的图片还原
            for t_sprite in self.box_terminal_group.sprites():
                if not t_sprite.is_success:
                    t_sprite.image = pygame.image.load(TERMINAL_IMAGE)

    def __box_wall_box_collide(self, box_sprite):
        # 游戏箱子与墙发生碰撞时,游戏箱子保持原位不动,游戏角色也保持不动
        result = pygame.sprite.groupcollide(self.box_group, self.wall_group, False, False)
        # 游戏箱子与游戏箱子发送碰撞时,游戏箱子保持原位不动,游戏角色也保持不动
        # 先移除与自己相比的精灵,不然会一直都有碰撞
        self.box_group.remove(box_sprite[0])
        box_collide_result = pygame.sprite.spritecollide(box_sprite[0], self.box_group, False)
        print(box_collide_result)
        if result or box_collide_result:
            print("test")
            if self.move_direction == "up":
                box_sprite[0].rect.y = box_sprite[0].rect.y + box_sprite[0].rect.height
            elif self.move_direction == "down":
                box_sprite[0].rect.y = box_sprite[0].rect.y - box_sprite[0].rect.height
            elif self.move_direction == "left":
                box_sprite[0].rect.x = box_sprite[0].rect.x + box_sprite[0].rect.width
            elif self.move_direction == "right":
                box_sprite[0].rect.x = box_sprite[0].rect.x - box_sprite[0].rect.width
            self.__back_person()
        # 记得把移除完的游戏箱子精灵也加回来不然箱子会消失
        self.box_group.add(box_sprite[0])

    def __back_person(self):
        """根据游戏角色移动方向的相反方向回退保持原位不动"""
        if self.move_direction == "up":
            self.game_person_sprite.move_down()
        elif self.move_direction == "down":
            self.game_person_sprite.move_up()
        elif self.move_direction == "left":
            self.game_person_sprite.move_right()
        elif self.move_direction == "right":
            self.game_person_sprite.move_left()

    def __move_event(self, event):
        """游戏角色移动事件处理"""

        # 游戏角色与墙发生碰撞,游戏角色(回退)保持原位不动
        wall_sprite = pygame.sprite.spritecollide(self.game_person_sprite, self.wall_group, False)
        print(wall_sprite)
        if event.key == pygame.K_w or pygame.key.name(event.key) == "up":
            # 记录移动方向
            self.move_direction = pygame.key.name(event.key)
            self.game_person_sprite.move_up()
        elif event.key == pygame.K_s or pygame.key.name(event.key) == "down":
            self.move_direction = pygame.key.name(event.key)
            self.game_person_sprite.move_down()
        elif event.key == pygame.K_a or pygame.key.name(event.key) == "left":
            self.move_direction = pygame.key.name(event.key)
            self.game_person_sprite.move_left()
        elif event.key == pygame.K_d or pygame.key.name(event.key) == "right":
            self.move_direction = pygame.key.name(event.key)
            self.game_person_sprite.move_right()

    def __init_game_map(self):
        """初始游戏地图"""
        self.is_first = True
        box_count = 0
        terminal_count = 0
        wall_count = 0
        for x in range(len(self.game_map)):
            for y in range(len(self.game_map[x])):
                if self.game_map[x][y] == BOX_FLAG:
                    box_count += 1
                elif self.game_map[x][y] == TERMINAL_FLAG:
                    terminal_count += 1
                elif self.game_map[x][y] == WALL_FLAG:
                    wall_count += 1
        self.box_counts = box_count
        self.wall_counts = wall_count
        self.terminal_counts = terminal_count

    def __update_game_level(self):
        """更新游戏关卡"""
        count = 0
        for terminal_sprite in self.box_terminal_group.sprites():
            if terminal_sprite.is_success:
                count += 1
        # 如果目的地全部变成星星图片则下一关卡
        if count == self.terminal_counts:
            # 由于while速度太快，加个是否第一次的标志来更新关卡
            if self.is_first:
                self.game_level += 1
                self.is_first = False
                level = self.game_level
                print("游戏关卡:" + str(self.game_level))
                # 释放内存
                del self
                BoxGame(game_level=level).start_game()


if __name__ == '__main__':
    BoxGame().start_game()
    pass
