/* -*- c++ -*- */
/*
 * Copyright 2022 Clayton Smith.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DSDCC_DSDCC_BLOCK_IMPL_H
#define INCLUDED_DSDCC_DSDCC_BLOCK_IMPL_H

#include "dsdcc/dsd_decoder.h"
#include <gnuradio/dsdcc/dsdcc_block.h>
#include <queue>

namespace gr {
namespace dsdcc {

class dsdcc_block_impl : public dsdcc_block
{
private:
    DSDcc::DSDDecoder dsdDecoder;
    std::queue<short> queue1;
    std::queue<short> queue2;

public:
    dsdcc_block_impl(DSDDecodeMode mode);
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
