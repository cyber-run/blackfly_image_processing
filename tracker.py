import math


class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

        self.t = 1/10

        self.scale = 3.45

    def update(self, objects_rect):
        # Initialise empty array to store box parameters and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h, vel = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            # Loops through existing center points stored in array and checks if current parsed new box and center
            # point is within 80 pixels of a center point that is currently stored
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                # If distance is less than 80 pixels, assume the newly detected particle is this old stored one and
                # add it back to new array with existing particle ID
                if dist < 80:
                    self.center_points[id] = (cx, cy)
                    # print(self.center_points)
                    vel = (cx - pt[0]) * self.t * self.scale
                    objects_bbs_ids.append([x, y, w, h, id, vel])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count, 0])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id, _ = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids
