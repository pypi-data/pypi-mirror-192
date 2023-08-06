# -*- coding=utf-8 -*-

"""Tests for index library."""

# XXX: which convention for integration testing?
from revsymg.index_lib import (
    FORWARD_INT,
    REVERSE_INT,
    eindor_orientation,
    is_canonical,
    is_forward,
    is_reverse,
    rev_edge,
    rev_vertex,
)
from tests.datatest import U_F, U_R, V_F, V_R


# ============================================================================ #
#                                TEST FUNCTIONS                                #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                                  Is_forward                                  #
# ---------------------------------------------------------------------------- #
def test_is_forward():
    """Test is_forward function."""
    assert is_forward(U_F)
    assert not is_forward(U_R)


# ---------------------------------------------------------------------------- #
#                                  Is_reverse                                  #
# ---------------------------------------------------------------------------- #
def test_is_reverse():
    """Test is_reverse function."""
    assert not is_reverse(U_F)
    assert is_reverse(U_R)


# ---------------------------------------------------------------------------- #
#                                  Rev_vertex                                  #
# ---------------------------------------------------------------------------- #
def test_rev_vertex():
    """Test rev_vertex function."""
    assert rev_vertex(U_F) == U_R
    assert rev_vertex(U_R) == U_F


# ---------------------------------------------------------------------------- #
#                                   Rev_edge                                   #
# ---------------------------------------------------------------------------- #
def test_rev_edge():
    """Test rev_edge function."""
    assert rev_edge(U_F, V_F) == (V_R, U_R)
    assert rev_edge(V_R, U_R) == (U_F, V_F)


# ---------------------------------------------------------------------------- #
#                                 Is_canonical                                 #
# ---------------------------------------------------------------------------- #
def test_is_canonical():
    """Test is_canonical function."""
    assert is_canonical(U_F, V_F)
    assert not is_canonical(V_R, U_R)
    assert is_canonical(V_F, U_F)
    assert not is_canonical(U_R, V_R)
    assert is_canonical(U_F, V_R)
    assert not is_canonical(V_F, U_R)
    assert is_canonical(U_R, V_F)
    assert not is_canonical(V_R, U_F)


# ---------------------------------------------------------------------------- #
#                              Eindor_orientation                              #
# ---------------------------------------------------------------------------- #
def test_eindor_orientation():
    """Test eindor_orientation function."""
    assert eindor_orientation(U_F, V_F) == FORWARD_INT
    assert eindor_orientation(V_F, U_F) == REVERSE_INT
    assert eindor_orientation(U_F, U_R) == FORWARD_INT
    assert eindor_orientation(U_R, U_F) == REVERSE_INT
    assert eindor_orientation(U_F, U_F) == FORWARD_INT
    assert eindor_orientation(U_R, U_R) == REVERSE_INT
