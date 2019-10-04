# -*- Coding:UTF-8 -*-
"""
游戏精灵模块
author:Mr Liu
version:1.0
"""

import pygame

# 游戏窗口大小
SCREEN_RECT = pygame.Rect(0, 0, 300, 300)
# 游戏名称
GAME_NAME = "BoxGame"
# 游戏刷新帧率
FRAME_PRE_SEC = 60
# 游戏背景图片
GAME_BACKGROUND = "image/white_bg.png"
# 游戏角色图片
PERSON_IMAGE = "image/human.png"
# 游戏箱子图片
BOX_IMAGE = "image/box.png"
# 箱子到达终点时星星图片
STAR_IMAGE = "image/star.png"
# 终点图片
TERMINAL_IMAGE = "image/terminal.png"
# 目的地与游戏重叠的图片
TERMINAL_PERSON_IMAGE = "image/t_man.png"
# 游戏墙图片
GAME_WALL = "image/wall.png"

# # 0	# 表示空
# WALL_FLAG = 1	        # 表示墙
# PERSON_FLAG = 2	        # 表示人
# BOX_FLAG = 3	        # 表示箱子
# TERMINAL_FLAG = 4	    # 表示目的地（球）
# FINISH_BOX_FLAG = 5	    # 表示已完成的箱子


# 9	# 表示空
WALL_FLAG = 1	        # 表示墙
PERSON_FLAG = 3	        # 表示人
BOX_FLAG = 2	        # 表示箱子
TERMINAL_FLAG = 4	    # 表示目的地（球）
FINISH_BOX_FLAG = 5	    # 表示已完成的箱子


class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""

    def __init__(self, image, game_map):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.game_map = game_map
        # 标识游戏箱子到达目的地
        self.is_success = False

    # def set_pos(self, x, y):
    #     """设置位置"""
    #     self.rect.x = x
    #     self.rect.y = y

    def set_sprite_pos(self, sprite_counts, sprite_flag):
        """
        设置精灵的位置
        :param sprite_counts:精灵出现的数量
        :param sprite_flag:精灵的标记
        :return:
        """
        count = 0
        for x in range(len(self.game_map)):
            for y in range(len(self.game_map[x])):
                if self.game_map[x][y] == sprite_flag:
                    # 根据箱子的第几个数数量来设置位置
                    if count == sprite_counts:
                        self.rect.x = self.rect.width * x
                        self.rect.y = self.rect.height * y
                        return
                    count += 1


class GamePerson(GameSprite):
    """游戏角色精灵"""

    def __init__(self, image, game_map):
        super().__init__(image, game_map)
        self.person_x = self.rect.x
        self.person_y = self.rect.y
        # 设置游戏角色位置
        super().set_sprite_pos(0, PERSON_FLAG)

    # def set_pos(self):
    #     """设置游戏角色位置"""
    #     for x in range(len(self.game_map)):
    #         for y in range(len(self.game_map)):
    #             if self.game_map[x][y] == 2:
    #                 super().set_pos(x=self.rect.width * x, y=self.rect.height * y)

    def move_left(self):
        """向右移动"""
        self.rect.x = self.rect.x - self.rect.width
        pass

    def move_right(self):
        """向左移动"""
        self.rect.x = self.rect.x + self.rect.width
        pass

    def move_up(self):
        """向上移动"""
        self.rect.y = self.rect.y - self.rect.height
        pass

    def move_down(self):
        """向下移动"""
        self.rect.y = self.rect.y + self.rect.height
        pass


class Box(GameSprite):
    """游戏箱子精灵"""

    def __init__(self, image, game_map):
        super().__init__(image, game_map)
        pass