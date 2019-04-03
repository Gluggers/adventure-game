import language
import items
import logging

DEFAULT_MAX_INVENT_SIZE = 120 #30 #40?
DEFAULT_MAX_ITEM_LISTING_SIZE = 200

class ItemListing(object):
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
            max_size=DEFAULT_MAX_ITEM_LISTING_SIZE,
        ):
        # Will be lists of 2-tuple (item_id, quantity).
        self._item_listing_data = []
        self._max_size = max_size

    @property
    def item_listing_data(self):
        return self._item_listing_data

    @property
    def max_size(self):
        return self._max_size

    def is_full(self):
        """Returns True if listing is full, False otherwise."""
        if len(self._item_listing_data) >= self._max_size:
            return True
        else:
            return False

    def get_current_size(self):
        return len(self._item_listing_data)

    def get_last_index(self):
        return len(self._item_listing_data) - 1

    # Given item_id, returns first index where the item ID first appears
    # in the inventory.
    # Returns -1 if item ID doesn't appear in inventory.
    def get_item_index(self, item_id):
        ret_index = -1

        curr_index = 0
        found = False
        curr_size = self.get_current_size()

        while (curr_index < curr_size) and (not found):
            curr_item_id = self._item_listing_data[curr_index][0]
            if curr_item_id == item_id:
                found = True
                ret_index = curr_index
            else:
                curr_index += 1

        return ret_index

    def has_item(self, item_id):
        if self.get_item_index(item_id) >= 0:
            return True
        else:
            return False

    # Sorts alphabetically according to the current set language.
    def alphabetical_sort(self, reverse=False):
        self._item_listing_data.sort(
            reverse=reverse,
            key=lambda x: items.Item.get_item(x[0]).get_name()
        )

    # Sorts stackable items first in order from least to greatest
    # item ID number. Then sorts non-stackable items together in order from
    # least to greatest item ID number.
    def standard_sort(self):
        stackables = []
        nonstackables = []
        final_list = []

        for item_data in self._item_listing_data:
            item_id = item_data[0]
            curr_item = items.Item.get_item(item_id)

            if curr_item:
                if curr_item.is_stackable():
                    stackables.append(item_data)
                else:
                    nonstackables.append(item_data)
            else:
                logger.error("Invalid item with id {0} in listing.".format(item_id))

        stackables.sort(
            key=lambda x: x[0]
        )
        nonstackables.sort(
            key=lambda x: x[0]
        )

        for data in stackables:
            final_list.append(data)
        for data in nonstackables:
            final_list.append(data)

        self._item_listing_data = final_list

    # Mainly for debugging purposes.
    def print_self(self):
        for item_entry in self._item_listing_data:
            item_id = item_entry[0]
            item_obj = items.Item.get_item(item_id)

            if item_obj:
                item_name = item_obj.get_name()
                print("Item ID: {0}; name: {1}; quantity: {2}".format(
                    item_id,
                    item_name,
                    item_entry[1]
                ))
            else:
                logger.error("Invalid item ID {0}".format(item_id))

    # Adds item to inventory. Returns True upon success, False on failure.
    # Child must override this method.
    def add_item(
            self,
            item_id,
            quantity=1,
        ):
        return False

    # Child must override.
    def remove_item_by_index(
            self,
            index,
            quantity=1,
        ):
        pass

    def remove_item_all(
            self,
            item_id
        ):
        if item_id is not None:
            # Get current quantity.
            curr_quantity = self.get_item_quantity(item_id)

            if curr_quantity:
                self.remove_item(
                    item_id,
                    quantity=curr_quantity,
                )

    def remove_item(
            self,
            item_id,
            quantity=1,
        ):
        if quantity > 0 and (item_id is not None):
            # Make sure item ID is valid.
            entry_index = self.get_item_index(item_id)

            if entry_index >= 0:
                self.remove_item_by_index(
                    entry_index,
                    quantity=quantity,
                )
            else:
                logger.warn("Trying to remove item that isn't in inventory.")

    # Child must override.
    def get_item_quantity(self, item_id):
        pass

    def get_item_entry(self, index):
        ret_val = None

        if index is not None:
            ret_val = self._item_listing_data[index]

        return ret_val

class StackedItemListing(ItemListing):
    def __init__(
            self,
            max_size=DEFAULT_MAX_ITEM_LISTING_SIZE,
        ):
        # Will be lists of 2-tuple (item_id, quantity).
        # Non-stackable items will have quantity of 1 and will be
        # in separate tuples, while stackable items with the same ID
        # will share the same tuple and can have a quantity value
        # of greater than 1.
        # Quantity should not be less than 1, otherwise item will be
        # removed from the data structure.
        ItemListing.__init__(
            self,
            max_size=max_size,
        )

class Inventory(ItemListing):
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
        # Will be lists of 2-tuple (item_id, quantity).
        # Non-stackable items will have quantity of 1 and will be
        # in separate tuples, while stackable items with the same ID
        # will share the same tuple and can have a quantity value
        # of greater than 1.
        # Quantity should not be less than 1, otherwise item will be
        # removed from the data structure.
        ItemListing.__init__(
            self,
            max_size=max_size,
        )

    # Overridden.
    def add_item(
            self,
            item_id,
            quantity=1,
        ):
        success = False
        num_to_add = quantity

        # Make sure item_id is valid.
        item_obj = items.Item.get_item(item_id)

        if item_obj:
            if num_to_add:
            # Check if the object is stackable.
                if item_obj.is_stackable():
                    # Check if we already have the object in the inventory.
                    item_index = self.get_item_index(item_id)

                    if item_index >= 0:
                        # We have the object. Increase quantity.
                        item_data = self._item_listing_data[item_index]
                        old_quantity = item_data[1]

                        new_quantity = old_quantity + num_to_add
                        self._item_listing_data[item_index] = (
                            item_id,
                            new_quantity,
                        )

                        logger.info("Prev {2} quantity: {0}. New quantity: {1}".format(
                            old_quantity,
                            self._item_listing_data[item_index][1],
                            item_obj.get_name(),
                        ))

                        success = True
                    elif self.is_full():
                        # Can't fit new slot.
                        logger.warn("Trying to add new item to full inventory.")
                    else:
                        # We can make a new inventory entry for this item.
                        self._item_listing_data.append((
                            item_id,
                            num_to_add,
                        ))
                        success = True
                else:
                    # Not stackable. Make a new inventory entry for the item
                    # if we can. Number of new entries is number of items.
                    if self.is_full():
                        # Can't fit new slot.
                        logger.warn("Trying to add new item to full inventory.")
                    else:
                        remaining_spaces = self.max_size \
                                        - self.get_current_size()
                        num_to_add = min(remaining_spaces, quantity)
                        if num_to_add < quantity:
                            # Can't fit all items.
                            logger.warn("Can't add all items to inventory.")

                        for i in range(num_to_add):
                            # We can make a new inventory entry for this item.
                            self._item_listing_data.append((
                                item_id,
                                1
                            ))

                        success = True
        else:
            logger.error("Invalid item ID {0}".format(item_id))

        if success:
            logger.info("Added item {0} x{1} to inventory.".format(
                item_obj.get_name(),
                num_to_add,
            ))

        return success

    # Overridden.
    def remove_item_by_index(
            self,
            index,
            quantity=1,
        ):
        if quantity > 0 and (index is not None) \
                and index >= 0 and index <= self.get_last_index():
            item_entry = self._item_listing_data[index]
            item_id = item_entry[0]
            item_obj = items.Item.get_item(item_id)
            old_quantity = None

            if item_obj:
                if item_obj.is_stackable():
                    old_quantity = item_entry[1]
                else:
                    old_quantity = self.get_item_quantity(item_id)

                new_quantity = max(0, old_quantity - quantity)

                if item_obj.is_stackable():
                    if new_quantity > 0:
                        self._item_listing_data[index] = (
                            item_id,
                            new_quantity,
                        )
                    else:
                        self._item_listing_data.pop(index)
                else:
                    # Handle nonstackable item.
                    self._item_listing_data.pop(index)
                    to_remove = old_quantity - new_quantity - 1

                    curr_index = self.get_last_index()
                    early_finish = False

                    while to_remove > 0 and curr_index >= 0:
                        curr_entry = self._item_listing_data[curr_index]
                        if curr_entry[0] == item_id:
                            self._item_listing_data.pop(curr_index)
                            to_remove -= 1

                        curr_index -= 1

                logger.info("Removed {0} x{1}".format(
                    item_obj.get_name(),
                    old_quantity - self.get_item_quantity(item_id)
                ))
            else:
                logger.error(
                    "Trying to remove invalid item ID from inventory.".format(
                        item_id
                    )
                )

    # Overridden.
    def get_item_quantity(self, item_id):
        quantity = 0

        item_obj = items.Item.get_item(item_id)

        if item_obj:
            if item_obj.is_stackable():
                obj_index = self.get_item_index(item_id)

                if obj_index >= 0:
                    entry = self._item_listing_data[obj_index]
                    quantity = entry[1]
            else:
                num_found = 0
                for entry in self._item_listing_data:
                    curr_obj = entry[0]
                    if entry[0] == item_id:
                        num_found += entry[1]

                quantity = num_found
        else:
            logger.error("Invalid item ID {0}".format(item_id))

        return quantity

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
