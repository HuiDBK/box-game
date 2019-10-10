# -*- Coding:UTF-8 -*-
"""
推箱子游戏主模块
author:Mr Liu
version:1.0
"""

import os
import sys
import time
import random
import pyautogui as gui
from game_sprites import *

pygame.init()


def random_music():
    """随机播放音乐"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(random.choice(GAME_MUSICS))
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        print("无法加载音频设置，请检查电脑配置\t" + str(e))
        # 打印异常行数
        print("Line_Num:" + str(e.__traceback__.tb_lineno))


random_music()

# 获取电脑屏幕分辨率
screen_width, screen_height = gui.size()
game_x = (screen_width - SCREEN_RECT.width) / 2
game_y = (screen_height - SCREEN_RECT.height) / 2
# 设置游戏窗口相对电脑屏幕居中
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_x, game_y)


class BoxGame(object):
    """推箱子游戏主类"""

    def __init__(self, game_level=1):
        # 标识是否第一次开启时间计时
        self.is_first_time_count = True
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 设置游戏名称和图标
        self.game_name = pygame.display.set_caption(GAME_NAME)
        pygame.display.set_icon(pygame.image.load(GAME_ICON))
        self.game_clock = pygame.time.Clock()
        # 默认游戏关卡为1
        self.game_level = game_level
        self.game_map = game_maps[self.game_level]
        self.is_first = True
        # 记录游戏角色移动方向
        self.move_direction = None
        # 记录游戏开始时间
        self.start_time = None
        # 记录游戏当前时间
        self.current_time = None
        # 记录游戏移动步数
        self.step_count = 0
        # 初始化游戏地图
        self.__init_game_map()
        self.__create_sprite()
        # 设置音乐结束事件
        try:
            pygame.mixer.music.set_endevent(MUSICS_END_EVENT)
        except Exception as e:
            print("无法设置音乐结束事件\t" + str(e))
            print("Line_Num:" + str(e.__traceback__.tb_lineno))

    def start_game(self):
        """游戏开始"""
        while True:
            self.game_clock.tick(FRAME_PRE_SEC)
            self.__event_handle()
            self.current_time = time.process_time()
            self.__check_collision()
            self.__update_sprite()
            self.__update_game_level()
            pygame.display.update()
            pass

    def __event_handle(self):
        """游戏事件监听"""
        for event in pygame.event.get():
            try:
                if pygame.mixer.music.get_endevent() == MUSICS_END_EVENT and not pygame.mixer.music.get_busy():
                    print("下一首")
                    music_file = random.choice(GAME_MUSICS)
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play(loops=0)
            except Exception as e:
                print("无法加载音频，请检查电脑配置\t" + str(e))
                print("Line_Num:" + str(e.__traceback__.tb_lineno))
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # print(pygame.key.name(event.key))
                self.__move_event(event)
                self.__time_step_count(event)
            elif event.type == pygame.KEYUP:
                print("keyup")
            elif event.type == pygame.MOUSEMOTION:
                # 鼠标移动事件
                x, y = event.pos  # 获取屏幕坐标位置
                # print("Mouse_Move:%s---%s" % (x, y))
                if self.__is_on_reset_img(x, y):
                    # 更换蓝颜色的重玩图片
                    self.reset_sprite_group.sprites()[0].image = pygame.image.load(BLUE_RESET_IMG)
                else:
                    # 还原
                    self.reset_sprite_group.sprites()[0].image = pygame.image.load(RED_RESET_IMG)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 鼠标点击事件
                x, y = event.pos  # 获取鼠标点击屏幕时的坐标位置
                print("Mouse_Click:%s---%s" % (x, y))
                if self.__is_on_reset_img(x, y):
                    # 开启重玩
                    self.__reset_game()

    @staticmethod
    def __is_on_reset_img(x, y):
        """
        判断鼠标位置是否在重玩图片上
        :param x:
        :param y:
        :return:boolean
        """
        if (RESET_IMG_POS.x <= x <= RESET_IMG_POS.x + RESET_IMG_POS.width) and \
                (RESET_IMG_POS.y <= y <= RESET_IMG_POS.y + RESET_IMG_POS.height):
            return True
        else:
            return False

    def __create_sprite(self):
        # 创建游戏背景
        game_bg_sprite = GameSprite(GAME_BACKGROUND, self.game_map)
        # 这样可以适应用户更改游戏背景图片但是可能会变形
        game_bg_sprite.image = pygame.transform.scale(game_bg_sprite.image,
                                                      (SCREEN_RECT.width, SCREEN_RECT.height))
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

        # 创建显示游戏关卡精灵
        level_sprite = TextSprite(text="关卡: " + str(self.game_level))
        level_sprite.set_rect(LEVEL_DISPLAY_POS)
        self.level_sprite_group = pygame.sprite.Group(level_sprite)

        # 创建显示时间精灵
        time_sprite = TextSprite(text="Time: 0")
        time_sprite.set_rect(TIME_DISPLAY_POS)
        self.time_sprite_group = pygame.sprite.Group(time_sprite)

        # 创建显示移动步数精灵
        step_sprite = TextSprite(text="Step: 0")
        step_sprite.set_rect(STEP_DISPLAY_POS)
        self.step_sprite_group = pygame.sprite.Group(step_sprite)

        # 创建重玩游戏精灵
        reset_sprite = GameSprite(RED_RESET_IMG, self.game_map)
        reset_sprite.set_pos(RESET_IMG_POS.x, RESET_IMG_POS.y)
        self.reset_sprite_group = pygame.sprite.Group(reset_sprite)

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

        if self.current_time is not None and self.start_time is not None:
            self.time_sprite_group.update("Time: " + str(self.current_time - self.start_time))
        self.time_sprite_group.draw(self.screen)

        self.step_sprite_group.update("Step: " + str(self.step_count))
        self.step_sprite_group.draw(self.screen)

        self.level_sprite_group.draw(self.screen)

        self.reset_sprite_group.draw(self.screen)

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
        # 步数回退
        self.step_count -= 1
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
        if event.key == pygame.K_w or pygame.key.name(event.key) == "up":
            # 记录移动方向
            self.move_direction = "up"
            self.game_person_sprite.move_up()
        elif event.key == pygame.K_s or pygame.key.name(event.key) == "down":
            self.move_direction = "down"
            self.game_person_sprite.move_down()
        elif event.key == pygame.K_a or pygame.key.name(event.key) == "left":
            self.move_direction = "left"
            self.game_person_sprite.move_left()
        elif event.key == pygame.K_d or pygame.key.name(event.key) == "right":
            self.move_direction = "right"
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
                if self.game_map[x][y] == TERMINAL_FLAG:
                    terminal_count += 1
                if self.game_map[x][y] == WALL_FLAG:
                    wall_count += 1
        # print("box_count:" + str(box_count))
        # print("wall_count" + str(wall_count))
        # print("terminal_count" + str(terminal_count))
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

    def __time_step_count(self, event):
        """游戏时间和移动步数计时"""
        if event.key == pygame.K_w or pygame.key.name(event.key) == "up" or \
                event.key == pygame.K_s or pygame.key.name(event.key) == "down" or \
                event.key == pygame.K_a or pygame.key.name(event.key) == "left" or \
                event.key == pygame.K_d or pygame.key.name(event.key) == "right":
            if self.is_first_time_count:
                self.start_time = time.process_time()
                self.is_first_time_count = False
            self.step_count += 1

    def __reset_game(self):
        """当前关卡重玩"""
        game_level = self.game_level
        if self.step_count == 0:
            # 如果玩家没有走动则重置无效
            print("玩家没有走动则重置无效")
            return
        del self    # 释放内存
        BoxGame(game_level=game_level).start_game()


if __name__ == '__main__':
    try:
        BoxGame().start_game()
    except Exception as e:
        print("未知异常\t" + str(e))
        print("Line_Num:" + str(e.__traceback__.tb_lineno))