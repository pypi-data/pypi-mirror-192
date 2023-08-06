import unittest

from .unet import UNet


class TestUNet(unittest.TestCase):
    def test_construct(self):
        unet = UNet(name="unet50_fmow_rgb")
        n_param = unet.num_params()

        self.assertEqual(n_param, 32541792)

        self.assertTrue(len(unet.describe()))
        self.assertEqual(unet.name, "unet50_fmow_rgb")

    @unittest.skip("Big download need to find a better unittest")
    def test_load(self):
        unet = UNet(name="unet50_fmow_rgb")
        n_param = unet.num_params()

        self.assertEqual(n_param, 32541792)
        self.assertTrue(len(unet.describe()))
        self.assertEqual(unet.name, "resnet50_rgb")

        unet.load_weights(
            encoder_weights="unet50_fmow_rgb", decoder_weights="unet50_fmow_rgb"
        )

    def test_fails(self):
        with self.assertRaises(Exception):
            _ = UNet(name="not_a_network")


if __name__ == "__main__":
    unittest.main()
