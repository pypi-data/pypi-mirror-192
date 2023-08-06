import json


def labelme_to_tlbr(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    gt_bb_list = list(map(lambda x: x['points'][0] + x['points'][1], data['shapes']))
    new_gt_bb_list = []
    for x0, y0, x1, y1 in gt_bb_list:
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        new_gt_bb_list.append((x0, y0, x1, y1))

    return new_gt_bb_list


def get_f1_score(prec, rec):
    return 2 * prec * rec / (prec + rec)


def intersection_over_union(boxA, boxB):
    # print(boxA, boxB)
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    if xB - xA < 0 or yB - yA < 0:
        return 0
    interArea = (xB - xA) * (yB - yA)

    # print(xA, yA, xB, yB)
    # print(interArea)

    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # return the intersection over union value
    return iou


