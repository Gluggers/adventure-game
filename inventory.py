import language
import items
import logging

DEFAULT_MAX_INVENT_SIZE = 120 #30 #40?

class Inventory():
    inventory_name_info = {
        language.LANG_ENGLISH: "Inventory",
        language.LANG_ESPANOL: "Inventario",
    }
    toolbelt_name_info = {
        language.LANG_ENGLISH: "Toolbelt",
        language.LANG_ESPANOL: "Herramientas",
    }

    def __init__(
                self,
                max_size=DEFAULT_MAX_INVENT_SIZE,
            ):
        # Will be lists of length-2 lists of the form
        # [item object, quantity].
        # Non-stackable items will have quantity of 1 and will be
        # in separate inner lists, while stackable items with the same ID
        # will share the same inner list and can have a quantity value
        # of greater than 1.
        # Quantity should not be less than 1, otherwise item will be
        # removed from the data structure.
        self.inventory_data = []

        self.max_size = DEFAULT_MAX_INVENT_SIZE
        if max_size and max_size > 0:
            self.max_size = max_size

    # Returns True if inventory is full, false otherwise.
    def is_full(self):
        if len(self.inventory_data) >= self.max_size:
            return True
        else:
            return False

    def current_size(self):
        return len(self.inventory_data)

    def get_last_index(self):
        return len(self.inventory_data) - 1

    # Given item_id, returns index for where the item ID first appears
    # in the inventory.
    # Returns -1 if item ID doesn't appear in inventory.
    def get_item_index(self, item_id):
        ret_index = -1

        curr_index = 0
        found = False
        inventory_size = len(self.inventory_data)

        while (curr_index < inventory_size) and (not found):
            curr_item_obj = self.inventory_data[curr_index][0]
            if curr_item_obj and (curr_item_obj.item_id == item_id):
                found = True
                ret_index = curr_index
            else:
                curr_index += 1

        return ret_index

    # Sorts alphabetically according to the current set language.
    def alphabetical_sort(self, reverse=False):
        self.inventory_data.sort(
            reverse=reverse,
            key=lambda x: x[0].get_name()
        )

    # Sorts stackable items first in order from least to greatest
    # item ID number. Then sorts non-stackable items together in order from
    # least to greatest item ID number.
    def standard_sort(self):
        stackables = []
        nonstackables = []
        final_list = []

        for data in self.inventory_data:
            if data[0].is_stackable():
                stackables.append(data)
            else:
                nonstackables.append(data)

        stackables.sort(
            key=lambda x: x[0].item_id
        )
        nonstackables.sort(
            key=lambda x: x[0].item_id
        )

        for data in stackables:
            final_list.append(data)
        for data in nonstackables:
            final_list.append(data)

        self.inventory_data = final_list

    # Adds item to inventory. Returns True upon success, False on failure.
    def add_item(
            self,
            item_obj,
            quantity=1,
        ):
        success = False

        if item_obj and quantity > 0:
            # Check if the object is stackable.
            if item_obj.is_stackable():
                # Check if we already have the object in the inventory.
                obj_index = self.get_item_index(item_obj.item_id)

                if obj_index >= 0:
                    # We have the object. Increase quantity.
                    inventory_entry = self.inventory_data[obj_index]
                    old_quantity = inventory_entry[1]

                    new_quantity = old_quantity + quantity
                    self.inventory_data[obj_index] = [
                        inventory_entry[0],
                        new_quantity
                    ]

                    logger.info("Prev {2} quantity: {0}. New quantity: {1}".format(
                        old_quantity,
                        self.inventory_data[obj_index][1],
                        self.inventory_data[obj_index][0].get_name(),
                    ))

                    success = True
                elif self.is_full():
                    # Can't fit new slot.
                    logger.warn("Trying to add new item to full inventory.")
                else:
                    # We can make a new inventory entry for this item.
                    self.inventory_data.append([
                        item_obj,
                        quantity
                    ])
                    success = True
            else:
                # Not stackable. Make a new inventory entry for the item
                # if we can. Number of new entries is number of items.
                if self.is_full():
                    # Can't fit new slot.
                    logger.warn("Trying to add new item to full inventory.")
                elif self.current_size() + quantity > self.max_size:
                    # Can't fit all items.
                    logger.warn("Can't add all items to inventory.")
                else:
                    for i in range(quantity):
                        # We can make a new inventory entry for this item.
                        self.inventory_data.append([
                            item_obj,
                            1
                        ])
                    success = True

        if success:
            logger.info("Added item {0} x{1} to inventory.".format(
                item_obj.get_name(),
                quantity
            ))

        return success

    # Adds item to inventory. Returns True upon success, False on failure.
    def add_item_by_id(
            self,
            item_id,
            quantity=1,
        ):
        success = False

        if quantity > 0 and (item_id is not None):
            # Make sure item ID is valid.
            item_obj = items.Item.get_item(item_id)

            if item_obj:
                success = self.add_item(
                    item_obj,
                    quantity=quantity,
                )
            else:
                logger.error(
                    "Trying to add invalid item ID {0} to inventory.".format(
                        item_id
                    )
                )

        return success

    # Mainly for debugging purposes.
    def print_self(self):
        for inventory_entry in self.inventory_data:
            item_obj = inventory_entry[0]
            item_id = item_obj.item_id
            item_name = item_obj.get_name()
            print("Item ID: {0}; name: {1}; quantity: {2}".format(
                item_id,
                item_name,
                inventory_entry[1]
            ))

    def remove_item(
            self,
            item_obj,
            quantity=1,
            remove_all_stackable=False,
            remove_all_nonstackable=False,
        ):
        # Check if we have the item to begin with.
        if item_obj and quantity > 0:
            self.remove_item_by_id(
                item_obj.item_id,
                quantity=quantity,
                remove_all_stackable=remove_all_stackable,
                remove_all_nonstackable=remove_all_nonstackable,
            )

    def remove_item_by_id(
            self,
            item_id,
            quantity=1,
            remove_all_stackable=False,
            remove_all_nonstackable=False,
        ):
        if quantity > 0 and (item_id is not None):
            # Make sure item ID is valid.
            entry_index = self.get_item_index(item_id)

            if entry_index >= 0:
                self.remove_item_by_index(
                    entry_index,
                    quantity=quantity,
                    remove_all_stackable=remove_all_stackable,
                    remove_all_nonstackable=remove_all_nonstackable,
                )
            else:
                logger.warn("Trying to remove item that isn't in inventory.")

    # TODO. Change so there is no remove_all flag? Caller has
    # to do quantity by hand?
    def remove_item_by_index(
            self,
            index,
            quantity=1,
            remove_all_stackable=False,
            remove_all_nonstackable=False,
        ):
        if quantity > 0 and (index is not None) \
                and index >= 0 and index <= len(self.inventory_data):
            inventory_entry = self.inventory_data[index]
            item_obj = inventory_entry[0]
            old_quantity = None

            if item_obj.is_stackable():
                old_quantity = inventory_entry[1]
            else:
                old_quantity = self.get_item_quantity(item_obj)

            new_quantity = max(0, old_quantity - quantity)

            if item_obj and old_quantity:
                if item_obj.is_stackable():
                    if new_quantity > 0 and not remove_all_stackable:
                        self.inventory_data[index] = [item_obj, new_quantity]
                    else:
                        self.inventory_data.pop(index)
                else:
                    # Handle nonstackable item.
                    self.inventory_data.pop(index)
                    to_remove = quantity - 1

                    if remove_all_nonstackable:
                        to_remove = old_quantity - 1

                    early_finish = False
                    while to_remove > 0 and not early_finish:
                        index = self.get_item_index(item_obj.item_id)
                        if index >= 0:
                            self.inventory_data.pop(index)
                        else:
                            early_finish = True

                        to_remove -= 1

            else:
                logger.error(
                    "Trying to remove invalid item ID from inventory.".format(
                        item_id
                    )
                )

    def get_item_quantity(self, item_obj):
        quantity = 0

        if item_obj:
            if item_obj.is_stackable():
                obj_index = self.get_item_index(item_obj.item_id)

                if obj_index >= 0:
                    entry = self.inventory_data[obj_index]
                    quantity = entry[1]
            else:
                num_found = 0
                for entry in self.inventory_data:
                    curr_obj = entry[0]
                    if curr_obj and item_obj.item_id == curr_obj.item_id:
                        num_found += entry[1]

                quantity = num_found

        return quantity

    def get_item_quantity_by_id(self, item_id):
        quantity = 0

        # Make sure item ID is valid.
        item_obj = items.Item.get_item(item_id)

        if item_obj:
            quantity = self.get_item_quantity(item_obj)
        else:
            logger.error(
                "Trying to query invalid item ID from inventory.".format(
                    item_id
                )
            )

        return quantity

    def has_item_id_in_inventory(self, item_id):
        if self.get_item_quantity_by_id(item_id):
            return True
        else:
            return False

    def has_item_in_inventory(self, item_obj):
        if self.get_item_quantity(item_obj):
            return True
        else:
            return False

    def get_item_entry(self, index):
        ret_val = None

        if index is not None:
            ret_val = self.inventory_data[index]

        return ret_val

    # initial_item_dict is mapping of item IDs to quantity. Used to
    # create initial inventory.
    # Returns created inventory.
    @classmethod
    def inventory_factory(
                cls,
                max_size=DEFAULT_MAX_INVENT_SIZE,
                initial_item_dict={},
            ):
        # Create inventory and populate initial items if any.
        ret_invent = Inventory(
            max_size=max_size,
        )

        if ret_invent and initial_item_dict:
            # Populate initial items if any.
            if initial_item_dict:
                for item_id, quantity in initial_item_dict.items():
                    ret_invent.add_item_by_id(item_id, quantity=quantity)
        return ret_invent

    @classmethod
    def get_inventory_name(cls, language_id):
        return cls.inventory_name_info.get(
            language_id,
            ""
        )

# set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
