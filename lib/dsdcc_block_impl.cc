/* -*- c++ -*- */
/*
 * Copyright 2022 Clayton Smith.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "dsdcc_block_impl.h"
#include <gnuradio/io_signature.h>
#include <cmath>

namespace gr {
namespace dsdcc {

using input_type = float;
using output_type = float;
dsdcc_block::sptr dsdcc_block::make(DSDDecodeMode mode)
{
    return gnuradio::make_block_sptr<dsdcc_block_impl>(mode);
}


/*
 * The private constructor
 */
dsdcc_block_impl::dsdcc_block_impl(DSDDecodeMode mode)
    : gr::block("dsdcc_block",
                gr::io_signature::make(
                    1 /* min inputs */, 1 /* max inputs */, sizeof(input_type)),
                gr::io_signature::make(
                    2 /* min outputs */, 2 /*max outputs */, sizeof(output_type)))
{
    dsdDecoder.setQuiet();

    switch (mode) {
    case DSDDecodeAuto:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeAuto, true);
        break;
    case DSDDecodeNone:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeNone, true);
        break;
    case DSDDecodeP25P1:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeP25P1, true);
        break;
    case DSDDecodeDStar:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeDStar, true);
        break;
    case DSDDecodeNXDN48:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeNXDN48, true);
        break;
    case DSDDecodeNXDN96:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeNXDN96, true);
        break;
    case DSDDecodeProVoice:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeProVoice, true);
        break;
    case DSDDecodeDMR:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeDMR, true);
        break;
    case DSDDecodeX2TDMA:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeX2TDMA, true);
        break;
    case DSDDecodeDPMR:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeDPMR, true);
        break;
    case DSDDecodeYSF:
        dsdDecoder.setDecodeMode(DSDcc::DSDDecoder::DSDDecodeYSF, true);
        break;
    }
}

/*
 * Our virtual destructor.
 */
dsdcc_block_impl::~dsdcc_block_impl() {}

void dsdcc_block_impl::forecast(int noutput_items, gr_vector_int& ninput_items_required)
{
    ninput_items_required[0] = noutput_items * 6;
}

int dsdcc_block_impl::general_work(int noutput_items,
                                   gr_vector_int& ninput_items,
                                   gr_vector_const_void_star& input_items,
                                   gr_vector_void_star& output_items)
{
    auto in = static_cast<const input_type*>(input_items[0]);
    auto out1 = static_cast<output_type*>(output_items[0]);
    auto out2 = static_cast<output_type*>(output_items[1]);

    for (int i = 0; i < noutput_items * 6; i++) {
        int nbAudioSamples1 = 0, nbAudioSamples2 = 0;
        short *audioSamples1, *audioSamples2;

        auto sample = static_cast<short>(std::lround(in[i] * 32768.0f));
        dsdDecoder.run(sample);

        audioSamples1 = dsdDecoder.getAudio1(nbAudioSamples1);
        if (nbAudioSamples1 > 0) {
            for (int i = 0; i < nbAudioSamples1; i++) {
                queue1.push(audioSamples1[i]);
            }
            dsdDecoder.resetAudio1();
        }

        audioSamples2 = dsdDecoder.getAudio2(nbAudioSamples2);
        if (nbAudioSamples2 > 0) {
            for (int i = 0; i < nbAudioSamples2; i++) {
                queue2.push(audioSamples2[i]);
            }
            dsdDecoder.resetAudio2();
        }
    }

    consume(0, noutput_items * 6);

    for (int i = 0; i < noutput_items; i++) {
        if (!queue1.empty()) {
            out1[i] = queue1.front() / 32768.0f;
            queue1.pop();
        } else {
            out1[i] = 0;
        }

        if (!queue2.empty()) {
            out2[i] = queue2.front() / 32768.0f;
            queue2.pop();
        } else {
            out2[i] = 0;
        }
    }

    return noutput_items;
}

} /* namespace dsdcc */
} /* namespace gr */
