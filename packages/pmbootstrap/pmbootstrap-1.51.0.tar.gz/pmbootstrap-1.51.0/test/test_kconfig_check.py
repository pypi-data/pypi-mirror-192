# Copyright 2023 Antoine Fontaine
# Copyright 2023 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import pytest
import sys

import pmb_test
import pmb_test.const
import pmb.parse.kconfig


@pytest.fixture
def args(tmpdir, request):
    import pmb.parse
    sys.argv = ["pmbootstrap.py", "kconfig", "check"]
    args = pmb.parse.arguments()
    args.log = args.work + "/log_testsuite.txt"
    pmb.helpers.logging.init(args)
    request.addfinalizer(pmb.helpers.logging.logfd.close)
    return args


def test_kconfig_check(args):
    # non-existing package
    assert pmb.parse.kconfig.check(args, "non-existing-kernel-package",
                                   must_exist=False) is None

    # basic checks, from easiers to hard-ish
    dir = f"{pmb_test.const.testdata}/kconfig_check/"
    assert not pmb.parse.kconfig.check_file(dir +
                                            "bad-missing-required-option")
    assert pmb.parse.kconfig.check_file(dir + "good")
    assert not pmb.parse.kconfig.check_file(dir + "bad-wrong-option-set")
    assert pmb.parse.kconfig.check_file(dir + "good-waydroid",
                                        waydroid=True)
    assert not pmb.parse.kconfig.check_file(dir +
                                            "bad-array-missing-some-options",
                                            waydroid=True)
    assert pmb.parse.kconfig.check_file(dir + "good-nftables",
                                        nftables=True)
    assert not pmb.parse.kconfig.check_file(dir + "bad-nftables",
                                            nftables=True)
    assert pmb.parse.kconfig.check_file(dir + "good-zram",
                                        zram=True)
    assert pmb.parse.kconfig.check_file(dir + "good-uefi",
                                        uefi=True)
    assert not pmb.parse.kconfig.check_file(dir + "bad-uefi",
                                            uefi=True)

    # tests on real devices
    # *** do not add more of these! ***
    # moving forward, tests in pmbootstrap.git should become more/completely
    # independent of the currently checked out pmaports.git (#2105)

    # it's a postmarketOS device, it will have the required options, and
    # supports nftables (with pmb:kconfigcheck-nftables)
    assert pmb.parse.kconfig.check(args, "nokia-n900")

    # supports Waydroid (with pmb:kconfigcheck-waydroid)
    assert pmb.parse.kconfig.check(args, "postmarketos-allwinner")

    # testing the force param: nokia-n900 will never need the uefi options
    assert not pmb.parse.kconfig.check(args, "nokia-n900",
                                       force_uefi_check=True)

    # supports zram (with pmb:kconfigcheck-zram), nftables
    assert pmb.parse.kconfig.check(args, "linux-purism-librem5")
