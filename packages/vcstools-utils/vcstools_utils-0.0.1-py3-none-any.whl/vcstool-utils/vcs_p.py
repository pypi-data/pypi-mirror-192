#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

#  Artem Smirnov by Promobot
#  TODO: to add auto complete function 
# see https://kislyuk.github.io/argcomplete


import git_works as gw
import work_args as wa
import parse_works as pa


def parse_work():
    args = wa.parse_args()

    if args.clear:
        gw.work_clear()

    if args.init:
        gw.work_init()

    if not pa.init_repos_json():
        return

    print("\nSync started... \n\n")
    gw.work_sync()
    print("\nSync completed! Working on direct command... \n\n")

    if pa.__ch_str(args.orep):
        gw.work_orep(args.orep)

    if args.oallrepos:
        gw.work_oallrepos()

    if pa.__ch_str(args.profile):
        gw.work_add_profile(args.profile)

    if pa.__ch_str(args.checkoutb):
        gw.work_checkoutb(args.checkoutb)

    if pa.__ch_str(args.checkout):
        gw.work_checkout(args.checkout)

    if pa.__ch_str(args.cfgb):
        pa.__switch_branch_cfg(args.cfgb)

    if args.show_repos:
        gw.work_show_repos()

    if args.fetch:
        gw.work_fetch()

    if args.status:
        gw.work_status()

    if args.pull:
        gw.work_pull()

    if args.push:
        gw.work_push()

    if args.sync:
        gw.work_sync()

    if args.add:
        gw.work_add()

    if args.commit:
        gw.work_commit()
