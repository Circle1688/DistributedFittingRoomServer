import json
import numpy as np


def get_adjusted_inputs(inputs):
    """
    Returns a dictionary of adjusted measurements.

    In this example, we:
      - Increase any measurement with 'Length' in its name by 2%.
      - Decrease any measurement with 'Size' in its name by 2%.
      - Leave the other values unchanged.

    You can modify the adjustment factors or logic as needed.
    """
    # # Original inputs.
    # inputs = {
    #     "Height": 180,
    #     "Thigh Length": 45.84773,
    #     "Calf Length": 46.71822,
    #     "Feet Length": 24.95818,
    #     "Neck Length": 11.30822,
    #     "Shoulder Width": 43.42514,
    #     "Upper Arm Length": 25.20014,
    #     "Forearm Length": 24.77694,
    #     "Hand Length": 18.56700,
    #     "Muscle": 0.25,
    #     "Body Fat": 0.20,
    #     "Neck Thickness": 32.21194,
    #     "Bust": 96.75247,
    #     "Cup": 15.09754,
    #     "Waist": 69.90949,
    #     "Belly": 80.75730,
    #     "Hips": 102.57145,
    #     "Thigh Size": 55.89947,
    #     "Calf Size": 36.81380,
    #     "Upper Arm Size": 25.16563,
    #     "Forearm Size": 22.76084,
    #     "Hand Size": 20.51066
    # }

    # Hand size and length mapping
    hand_size_adjustments = {
        "Small": 17.0,
        "Medium": 21.0,
        "Large": 25.0
    }

    hand_length_adjustments = {
        "Small": 15.0,
        "Medium": 19.0,
        "Large": 22.0
    }

    adjusted = {}
    for key, value in inputs.items():
        if key == "Hand Size":
            # Convert string size to numeric value
            adjusted[key] = hand_size_adjustments.get(value, 21.0)  # Default to Medium if invalid
        elif key == "Hand Length":
            # Convert string length to numeric value
            adjusted[key] = hand_length_adjustments.get(value, 19.0)  # Default to Medium if invalid
        elif key == "Underbust":
            # Convert Underbust to Cup (Cup = Bust - Underbust)
            adjusted["Cup"] = inputs["Bust"] - value
        else:
            # Leave all other measurements unchanged.
            adjusted[key] = value

    return adjusted


def compute_virtual_spine(basis, spine_row, spine_scale, keys):
    """Computes the virtual measurements at the spine level."""
    virtual = {}
    for k in keys:
        virtual[k] = basis[k] + 2 * (spine_row[k] - basis[k]) * (spine_scale - 1)
    return virtual


def compute_virtual(prev_virtual, basis, row, ctrl_key, real_value, keys):
    """Computes virtual measurements at subsequent levels using a K-value approach."""
    virtual = {}
    denom = row[ctrl_key] - basis[ctrl_key]
    if denom == 0:
        raise ValueError(f"Zero denominator for {ctrl_key} when computing K-values.")
    for k in keys:
        K = (row[k] - basis[k]) / denom
        virtual[k] = prev_virtual[k] + K * (real_value - prev_virtual[ctrl_key])
    return virtual


def compute_shape_keys(real, virtual_length, basis, size_rows, coeff_matrix, shape_key_map):
    """
    Computes shape key values based on size.
    
    1. Adjust the virtual measurements for body fat.
       If real Body Fat > basis Body Fat, use the 'overweight' row;
       else, use the 'skinny' row.
    2. For each measurement, the adjusted virtual value is:
         virtual_adjusted = virtual_length + K*(real Body Fat - virtual_length["Body Fat"])
       where K is computed from the chosen row.
    3. For the interdependent shape keys, a delta vector is formed:
         delta = real[measurement] - virtual_adjusted[measurement]
       for each measurement corresponding to a shape key.
    4. Then, the 13×13 system A * x = delta is solved using np.linalg.solve.
    """
    virtual_adjusted = {}
    if real["Body Fat"] > basis["Body Fat"]:
        row_used = size_rows["b_main_overweight"]
        b_main_overweight = ((real["Body Fat"] - basis["Body Fat"]) /
                             (row_used["Point1"]["Body Fat"] - basis["Body Fat"])) * row_used["ShapeKeyMultiplier"]
        b_main_skinny = 0
    else:
        row_used = size_rows["b_main_skinny"]
        b_main_skinny = ((real["Body Fat"] - basis["Body Fat"]) /
                         (row_used["Point1"]["Body Fat"] - basis["Body Fat"])) * row_used["ShapeKeyMultiplier"]
        b_main_overweight = 0

    for k in real:
        if k == "Body Fat":
            virtual_adjusted[k] = virtual_length[k]
        else:
            point1_val = row_used["Point1"].get(k, basis.get(k))
            K = (point1_val - basis.get(k, 0)) / (row_used["Point1"]["Body Fat"] - basis["Body Fat"])
            virtual_adjusted[k] = virtual_length[k] + K * (real["Body Fat"] - virtual_length["Body Fat"])
    
    muscular = size_rows["b_main_muscular"]
    if (muscular["Point1"]["Muscle"] - muscular["Basis"]["Muscle"]) == 0:
        b_main_muscular = 0
    else:
        b_main_muscular = ((real["Muscle"] - basis["Muscle"]) / (muscular["Point1"]["Muscle"] - muscular["Basis"]["Muscle"])) * muscular["ShapeKeyMultiplier"]
    
    shape_key_list = [
        "b_main_muscular",
        "b_Torso_Shoulder_Width",
        "b_Torso_Chest_Width",
        "b_Torso_Waist_Thickness",
        "b_Torso_Hips_Size",
        "b_Torso_Belly_Size",
        "b_Torso_Breast_Size",
        "b_Legs_Thigh_Thickness",
        "b_Arms_Upper_Arm_Thickness",
        "b_Legs_Shin_Thickness",
        "b_Arms_Forearm_Thickness",
        "b_Arms_Hand_Thickness",
        "b_Head_Neck_Thickness"
    ]
    delta_vector = []
    for sk in shape_key_list:
        meas = shape_key_map[sk]
        delta = real.get(meas, 0) - virtual_adjusted.get(meas, 0)
        delta_vector.append(delta)
    delta_vector = np.array(delta_vector)
    
    x = np.linalg.solve(coeff_matrix, delta_vector)
    
    shape_keys = {}
    for i, sk in enumerate(shape_key_list):
        shape_keys[sk] = x[i]
    
    shape_keys["b_main_overweight"] = b_main_overweight
    shape_keys["b_main_skinny"] = b_main_skinny
    shape_keys["b_main_muscular"] = b_main_muscular

    return virtual_adjusted, shape_keys


def male_converter(inputs):
    with open("converter/male_data.json", "r") as f:
        data = json.load(f)

    keys          = data["keys"]
    extra         = data["extra"]
    basis         = data["basis"]
    rows          = data["rows"]
    ctrl          = data["ctrl"]
    size_rows     = data["size_rows"]
    shape_key_map = data["shape_key_map"]
    coeff_matrix  = np.array(data["size_coeff_matrix"])

    # PART 1: Length-to-scale calculations.
    real = get_adjusted_inputs(inputs)

    real_torso = real["Height"] - extra["Head Length"] - real["Neck Length"] - real["Thigh Length"] - real["Calf Length"]
    spine_scale = real_torso / extra["Torso Length"]

    virtual_spine = compute_virtual_spine(basis, rows["spine"], spine_scale, keys)
    thigh_scale   = real["Thigh Length"] / virtual_spine["Thigh Length"]
    virtual_thigh = compute_virtual(virtual_spine, basis, rows["thigh"], ctrl["thigh"], real["Thigh Length"], keys)
    calf_scale    = real["Calf Length"] / virtual_thigh["Calf Length"]
    virtual_calf  = compute_virtual(virtual_thigh, basis, rows["calf"], ctrl["calf"], real["Calf Length"], keys)
    feet_scale    = real["Feet Length"] / virtual_calf["Feet Length"]
    virtual_feet  = compute_virtual(virtual_calf, basis, rows["feet"], ctrl["feet"], real["Feet Length"], keys)
    neck_scale    = real["Neck Length"] / virtual_feet["Neck Length"]
    virtual_neck  = compute_virtual(virtual_feet, basis, rows["neck"], ctrl["neck"], real["Neck Length"], keys)
    upper_arm_scale = real["Upper Arm Length"] / virtual_neck["Upper Arm Length"]
    virtual_upper_arm = compute_virtual(virtual_neck, basis, rows["upper_arm"], ctrl["upper_arm"], real["Upper Arm Length"], keys)
    forearm_scale = real["Forearm Length"] / virtual_upper_arm["Forearm Length"]
    virtual_forearm = compute_virtual(virtual_upper_arm, basis, rows["forearm"], ctrl["forearm"], real["Forearm Length"], keys)
    hand_scale    = real["Hand Length"] / virtual_forearm["Hand Length"]
    virtual_hand  = compute_virtual(virtual_forearm, basis, rows["hand"], ctrl["hand"], real["Hand Length"], keys)

    # PART 2: Shape key calculations.
    virtual_adjusted, shape_keys = compute_shape_keys(real, virtual_hand, basis, size_rows, coeff_matrix, shape_key_map)

    # Build the output JSON object.
    # Build "body_dimensions" using the specified order and mapping.
    ordered_shape_keys = [
      "b_{main}_overweight",
      "b_{main}_skinny",
      "b_{main}_muscular",
      "b_{Torso}_Shoulder Width",
      "b_{Torso}_Chest Width",
      "b_{Torso}_Waist Thickness",
      "b_{Torso}_Hips Size",
      "b_{Torso}_Belly Size",
      "b_{Torso}_Breast Size",
      "b_{Legs}_Thigh Thickness",
      "b_{Arms}_Upper Arm Thickness",
      "b_{Legs}_Shin Thickness",
      "b_{Arms}_Forearm Thickness",
      "b_{Arms}_Hand Thickness",
      "b_{Head}_Neck Thickness"
    ]
    shape_key_output_mapping = {
      "b_main_overweight": "b_{main}_overweight",
      "b_main_skinny": "b_{main}_skinny",
      "b_main_muscular": "b_{main}_muscular",
      "b_Torso_Shoulder_Width": "b_{Torso}_Shoulder Width",
      "b_Torso_Chest_Width": "b_{Torso}_Chest Width",
      "b_Torso_Waist_Thickness": "b_{Torso}_Waist Thickness",
      "b_Torso_Hips_Size": "b_{Torso}_Hips Size",
      "b_Torso_Belly_Size": "b_{Torso}_Belly Size",
      "b_Torso_Breast_Size": "b_{Torso}_Breast Size",
      "b_Legs_Thigh_Thickness": "b_{Legs}_Thigh Thickness",
      "b_Arms_Upper_Arm_Thickness": "b_{Arms}_Upper Arm Thickness",
      "b_Legs_Shin_Thickness": "b_{Legs}_Shin Thickness",
      "b_Arms_Forearm_Thickness": "b_{Arms}_Forearm Thickness",
      "b_Arms_Hand_Thickness": "b_{Arms}_Hand Thickness",
      "b_Head_Neck_Thickness": "b_{Head}_Neck Thickness"
    }
    body_dimensions = []
    for key in ordered_shape_keys:
        # Find the computed key that maps to this output key.
        comp_key = None
        for ck, out_key in shape_key_output_mapping.items():
            if out_key == key:
                comp_key = ck
                break
        value = shape_keys.get(comp_key, 0)
        # Format the value as a float with 10 decimal places.
        body_dimensions.append({"key": key, "value": float(f"{value:.10f}")})

    # Build "body_dimension_lengths" using the computed scales.
    bone_scale_mapping = {
      "spine": spine_scale,
      "thigh_R": thigh_scale,
      "thigh_L": thigh_scale,
      "shin_R": calf_scale,
      "shin_L": calf_scale,
      "foot_R": feet_scale,
      "foot_L": feet_scale,
      "neck": neck_scale,
      "upper_arm_R": upper_arm_scale,
      "upper_arm_L": upper_arm_scale,
      "forearm_R": forearm_scale,
      "forearm_L": forearm_scale,
      "hand_R": hand_scale,
      "hand_L": hand_scale
    }
    ordered_bones = [
      "spine",
      "thigh_R",
      "thigh_L",
      "shin_R",
      "shin_L",
      "foot_R",
      "foot_L",
      "neck",
      "upper_arm_R",
      "upper_arm_L",
      "forearm_R",
      "forearm_L",
      "hand_R",
      "hand_L"
    ]
    body_dimension_lengths = []
    for bone in ordered_bones:
        scale_val = bone_scale_mapping.get(bone, 1.0)
        if bone == "spine":
            bone_scale = {"x": float(f"{scale_val:.10f}"), "y": float(f"{scale_val:.10f}"), "z": float(f"{scale_val:.10f}")}
        else:
            bone_scale = {"x": 1.0, "y": float(f"{scale_val:.10f}"), "z": 1.0}
        body_dimension_lengths.append({"key": bone, "value": bone_scale})

    # Print the output JSON in the specified format:
    print("{")
    print('  "body_dimensions": [')
    for i, item in enumerate(body_dimensions):
        comma = "," if i < len(body_dimensions) - 1 else ""
        print("    " + json.dumps(item, separators=(',', ': ')) + comma)
    print("  ],")
    print('  "body_dimension_lengths": [')
    for i, item in enumerate(body_dimension_lengths):
        comma = "," if i < len(body_dimension_lengths) - 1 else ""
        print("    " + json.dumps(item, separators=(',', ': ')) + comma)
    print("  ]")
    print("}")

    return body_dimensions, body_dimension_lengths
