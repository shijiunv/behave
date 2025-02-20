# coding=utf-8

from .core import (
    BeNode,
    BeGeneratorAction,
    BeAction,
    BeCondition,
    BeSequence,
    BeSelect,
    BeDecorator,
    SUCCESS,
)
import inspect
from functools import wraps


# Functions for testing


def is_node(node):
    return isinstance(node, BeNode)


def is_sequence(node):
    return isinstance(node, BeSequence)


def is_selector(node):
    return isinstance(node, BeSelect)


def is_decorator(node):
    return isinstance(node, BeDecorator)


def is_condition(node):
    return isinstance(node, BeCondition)


def is_action(node):
    return isinstance(node, BeAction) or isinstance(node, BeGeneratorAction)


# 用于tree node定义的装饰器


def action(f):
    """动作节点装饰器"""
    if inspect.isgeneratorfunction(f):
        return BeGeneratorAction(f)
    else:
        return BeAction(f)


def condition(f):
    """条件节点装饰器"""
    return BeCondition(f)


def generator_decorator(f):
    """生成器装饰器, 待研究"""

    def ctor(bb, node):
        g = f(bb, node)

        def iter_func():
            try:
                return next(g)
            except StopIteration:
                return SUCCESS

        return iter_func

    return ctor


def decorator(f):
    """生成装饰器的装饰器"""
    if inspect.isgeneratorfunction(f):
        f = wraps(f)(generator_decorator(f))
    return BeDecorator([f])
