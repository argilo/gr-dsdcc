/* -*- c++ -*- */
/*
 * Copyright 2022 Clayton Smith.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DSDCC_DSDCC_BLOCK_IMPL_H
#define INCLUDED_DSDCC_DSDCC_BLOCK_IMPL_H

#include <gnuradio/dsdcc/dsdcc_block.h>

namespace gr {
namespace dsdcc {

class dsdcc_block_impl : public dsdcc_block
{
private:
    // Nothing to declare in this block.

public:
    dsdcc_block_impl(int foo);
    ~dsdcc_block_impl();

    // Where all the action really happens
    void forecast(int noutput_items, gr_vector_int& ninput_items_required);

    int general_work(int noutput_items,
                     gr_vector_int& ninput_items,
                     gr_vector_const_void_star& input_items,
                     gr_vector_void_star& output_items);
};

} // namespace dsdcc
} // namespace gr

#endif /* INCLUDED_DSDCC_DSDCC_BLOCK_IMPL_H */
