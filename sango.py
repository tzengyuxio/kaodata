import click
from utils import *


@click.group()
def san1():
    """三國志（初代）"""
    pass


@click.command(help='顏 CG 解析')
def san1_face():
    pass


san1.add_command(san1_face, 'face')

##############################################################################

@click.group()
def san2():
    """三國志II"""
    pass


@click.command(help='顏 CG 解析')
def san2_face():
    pass


san2.add_command(san2_face, 'face')

##############################################################################

@click.group()
def san3():
    """三國志III"""
    pass


@click.command(help='顏 CG 解析')
def san3_face():
    pass


san3.add_command(san3_face, 'face')
