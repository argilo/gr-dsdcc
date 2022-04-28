/* -*- c++ -*- */
/*
 * Copyright 2022 Clayton Smith.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_DSDCC_DSDCC_BLOCK_H
#define INCLUDED_DSDCC_DSDCC_BLOCK_H

#include <gnuradio/block.h>
#include <gnuradio/dsdcc/api.h>

namespace gr {
namespace dsdcc {

/*!
 * \brief <+description of block+>
 * \ingroup dsdcc
 *
 */
class DSDCC_API dsdcc_block : virtual public gr::block
{
public:
    typedef std::shared_ptr<dsdcc_block> sptr;

    /*!
     * \brief Return a shared_ptr to a new instance of dsdcc::dsdcc_block.
     *
     * To avoid accidental use of raw pointers, dsdcc::dsdcc_block's
     * constructor is in a private implementation
     * class. dsdcc::dsdcc_block::make is the public interface for
     * creating new instances.
     */
    static sptr make(int foo);
};

} // namespace dsdcc
} // namespace gr

#endif /* INCLUDED_DSDCC_DSDCC_BLOCK_H */
