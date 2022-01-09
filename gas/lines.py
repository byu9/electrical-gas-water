#!/usr/bin/env python3
from misc.unit_conversions import mcmph_to_mcfph

compressor_lines = {
    # (sending, receiving)
    ('entry03' , 'N01'),
    ('N04'     , 'N05'),
}

compressor_line_source_nodes = {s for (s, r) in compressor_lines}

# Per Xiaochu, to be approximated by piecewise-linear
def weymouth(psi_sq_s, psi_sq_r):
    diff = psi_sq_s - psi_sq_r
    mcf_per_hour = 0.8225 * diff + 4.692E-14
    return mcf_per_hour

# 3-segment piecewise linear
def weymouth3(psi_sq_s, psi_sq_r):
    diff = psi_sq_s - psi_sq_r
    mcf_per_hour = (
        (0.4728 * diff + 1279)      if diff >= 793 else
        (2.0850 * diff - 5.033E-14) if diff >= -793 else
        (0.4728 * diff - 1279)
    )
    return mcf_per_hour

flow_funcs = {
    # (s_node, r_node): callable(psi_sq_s, psi_sq_r) -> mcf_per_hour
    ('entry01' , 'entry03' ) : weymouth,
    ('N01'     , 'N02'     ) : weymouth,
    ('entry02' , 'N03'     ) : weymouth,
    ('N02'     , 'exit01'  ) : weymouth,
    ('N02'     , 'N04'     ) : weymouth,
    ('N03'     , 'N04'     ) : weymouth,
    ('N05'     , 'exit02'  ) : weymouth,
    ('N05'     , 'exit03'  ) : weymouth,
    ('N01'     , 'N03'     ) : weymouth,

    # compressor-enabled pipelines do not use flow functions
    # Placeholders
    ('entry03' , 'N01') : None,
    ('N04'     , 'N05') : None,
}


flow_lims = {
    # line: (mcf_per_hour_lo, mcf_per_hour_hi)
    ('entry01' , 'entry03' ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('N01'     , 'N02'     ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('entry02' , 'N03'     ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('N02'     , 'exit01'  ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('N02'     , 'N04'     ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('N03'     , 'N04'     ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('N05'     , 'exit02'  ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('N05'     , 'exit03'  ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('N01'     , 'N03'     ) : (mcmph_to_mcfph(-1100), mcmph_to_mcfph(1100)),
    ('entry03' , 'N01'     ) : (mcmph_to_mcfph(0),     mcmph_to_mcfph(1100)),
    ('N04'     , 'N05'     ) : (mcmph_to_mcfph(0),     mcmph_to_mcfph(1100)),
}

flow_lims_lo = dict()
flow_lims_hi = dict()
for line, (lo, hi) in flow_lims.items():
    flow_lims_lo[line] = lo
    flow_lims_hi[line] = hi
