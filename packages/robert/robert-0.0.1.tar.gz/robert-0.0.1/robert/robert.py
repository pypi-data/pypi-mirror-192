#!/usr/bin/env python

######################################################################.
######################################################################
###                                                                ###
###  ROBERT is a tool that allows to carry out automated:          ###
###  (CURATE) Curate the data                                      ###
###  (OUTLIERS) Outlier analysis                                   ###
###  (GENERATE) Optimize the ML model                              ###
###  (PREDICT) Predict new data                                    ###
###                                                                ###
######################################################################
###                                                                ###
###  Authors: Juan V. Alegre Requena, David Dalmau Ginesta         ###
###                                                                ###
###  Please, report any bugs or suggestions to:                    ###
###  jv.alegre@csic.es                                             ###
###                                                                ###
######################################################################
######################################################################.


from robert.curate import curate
# from robert.outliers import outliers
# from robert.generate import generate
# from robert.predict import predict
from robert.utils import command_line_args


def main():
    """
    Main function of AQME, acts as the starting point when the program is run through a terminal
    """

    # load user-defined arguments from command line
    args = command_line_args()
    args.command_line = True

    if not args.curate and not args.generate and not args.predict:
        print('x  No module was specified in the command line! (i.e. --cur for data curation).\n')

    # CURATE
    if args.curate:
        curate(
            input=args.varfile,
            varfile=args.varfile,
            command_line=args.command_line,
            destination=args.destination,
            csv_name=args.csv_name,
            y=args.y,
            discard=args.discard,
            categorical=args.categorical,
            corr_filter=args.corr_filter,
            thres_x=args.thres_x,
            thres_y=args.thres_y,
        )


            # max_workers=args.max_workers, for generate

if __name__ == "__main__":
    main()
