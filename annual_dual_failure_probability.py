"""annual_dual_failure_probability."""

import math

HOURS_PER_YEAR = 8760
HOUR = 1

# https://www.ti.com/lit/an/spraby3/spraby3.pdf?ts=1753039217595


def main() -> None:
    """Main function to run the program."""
    # indstry standerd fir 100-500
    # fit Failure In Time lower is better
    # https://docs.amd.com/r/en-US/ug116/Failure-Rate-Determination
    # https://product.tdk.com/en/contact/faq/power-supplies-0020.html
    # https://www.mitsubishielectric.com/semiconductors/powerdevices/application_notes/highpower_reliability_e.pdf

    cpu_mtbf = fit_to_mtbf(fit=500)
    # https://store.supermicro.com/us_en/800-1u-pws-802a-1r.html
    power_supply_mtbf = 200000

    # https://cdrdv2-public.intel.com/840480/S2600CW_TPS.pdf
    mobo_mtbf = 200000

    # https://americas.kioxia.com/en-us/business/ssd/enterprise-ssd/pm7-v.html
    ssd_mtbf = 2500000

    ram_mtbf = 1500000

    component_mttfs = {
        "CPU": cpu_mtbf,
        "Power Supply": redundant_mttf(power_supply_mtbf),
        "RAM": ram_mtbf,
        "SSD": redundant_mttf(ssd_mtbf),
        "Motherboard": mobo_mtbf,
    }

    system_mtbf = calculate_system_mtbf(component_mttfs)
    print(f"System MTBF: {system_mtbf:.0f} hours")

    for rto_hours in [4, 24, 48, 168]:
        joint_mtbf_hours, annual_probability = estimate_annual_dual_failure_probability(
            system_mtbf=system_mtbf,
            rto_hours=rto_hours,
        )
        print(f"RTO: {rto_hours} hours")
        print(f"Joint MTBF: {joint_mtbf_hours:.0f} hours")
        print(f"Annual probability of simultaneous failure: {annual_probability * 100:.5f}%")


def redundant_mttf(mttf: float) -> float:
    """Calculate MTTF for redundant components.

    Args:
    mttf: Mean Time To Failure for a single component in hours.

    Returns:
    Adjusted MTTF for redundant configuration.

    Note:
    Uses a 1.5x factor assuming N+1 redundancy with shared load.
    """
    return 1.5 * mttf


def calculate_system_mtbf(component_mttfs: dict) -> float:
    """Calculate the system MTBF (in hours) given component MTTFs.

    Args:
        component_mttfs (dict): A dictionary with component names as keys and MTTF values in hours as values.


    Returns:
        float: Estimated system MTBF in hours.
    """
    inverse_sum = 0.0
    for component, mttf in component_mttfs.items():
        if mttf <= 0:
            error = f"MTTF for {component} must be greater than 0"
            raise ValueError(error)
        inverse_sum += 1.0 / mttf

    if inverse_sum == 0:
        return float("inf")

    return 1.0 / inverse_sum


def estimate_annual_dual_failure_probability(system_mtbf: int, rto_hours: int) -> tuple[float, float]:
    """Estimate the probability of both nodes in a 2-node HA setup failing within the RTO window.

    Args:
        mtbf_hours (int): Mean Time Between Failures per node (in hours).
        rto_hours (int): Recovery Time Objective (i.e., the vulnerable window after one node fails).

    Returns:
        tuple[float, float]: A tuple containing:
            - joint_mtbf_hours: hours between expected simultaneous failures
            - annual_probability: annual chance of simultaneous failure (fraction)
    """
    failures_per_hour = HOUR / system_mtbf
    second_node_fault_rate = 1 - math.exp(-failures_per_hour * rto_hours)
    joint_failure_rate_per_hour = 2 * failures_per_hour * second_node_fault_rate
    joint_mtbf_hours = HOUR / joint_failure_rate_per_hour
    annual_probability = joint_failure_rate_per_hour * HOURS_PER_YEAR
    return joint_mtbf_hours, annual_probability


def fit_to_mtbf(fit: int) -> float:
    """Convert a FIT value (Failures In Time) to MTBF in hours.

    Args:
        fit (int): FIT value in failures per 10^9 hours

    Returns:
        float: MTBF in hours
    """
    return 1000000000 / fit


# https://www.intel.com/content/www/us/en/docs/programmable/683869/current/failure-rates.html

if __name__ == "__main__":
    main()
