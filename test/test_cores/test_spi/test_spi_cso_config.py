
from myhdl import instance, delay, StopSimulation
import rhea.cores.spi as spi
from rhea.cores.spi import spi_controller
from rhea.utils.test import run_testbench, tb_default_args


def test_spi_cso_config(args=None):
    args = tb_default_args()
    # get an instance of the control-status object
    cso = spi_controller.cso()
    assert isinstance(cso, spi.cso.SPIControlStatus)
    # set a default configuration
    cso.loopback.initial_value = False
    cso.clock_polarity.initial_value = True
    cso.clock_phase.initial_value = True
    cso.clock_divisor.initial_value = 2
    cso.slave_select.initial_value = 0x10
    cso.isstatic = True

    def bench():
        tbdut = cso.get_generators()

        @instance
        def tbstim():
            yield delay(10)
            assert not cso.loopback
            assert cso.clock_polarity
            assert cso.clock_phase
            assert cso.clock_divisor == 2
            assert cso.slave_select == 0x10
            yield delay(10)

            raise StopSimulation

        return tbdut, tbstim

    run_testbench(bench, args)


# @todo: this needs to become a decorator
def test_spi_cso(args=None):
    args = tb_default_args(args)

    def bench():
        @instance
        def tbstim():
            # @todo: add test stimulus
            yield delay(10)
            raise StopSimulation
        return tbstim

    run_testbench(bench, args)


if __name__ == '__main__':
    test_spi_cso_config()