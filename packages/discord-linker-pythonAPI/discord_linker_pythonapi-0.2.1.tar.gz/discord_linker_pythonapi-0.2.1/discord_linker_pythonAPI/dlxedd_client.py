import discord_linker_pythonAPI.wordpress_client as wpc



class DLXEDD_Client(wpc.WP_Client):
    """This class extends WP_Client and provides
    methods to use the dlxedd(discord-linker x easy-digital-downloads) api.

    This class provides access to more endpoints.
    Extra Endpoints:
        ["DLXEDD_CART"]

    Args:
        url (str): The URL of the website.
        user (str): The user we will use to connect.
        password (str): The application specific password.
    """

    def __init__(self, url:str, user:str, password:str):
        super().__init__(url, user, password)

        self.wp_endpoints["DLXEDD_CART"] = "/dlxedd/v1/cart"


    def cart_add(self, discord_id:str, product_id:str):
        """Add a product to the cart.

        Args:
            discord_id (str): The ID of the discord account.
            product_id (str): The ID of the product to add.
        """
        self.execute_and_check_errors("DLXEDD_CART", "add", [discord_id, product_id])


    def cart_remove(self, discord_id:str, product_id:str):
        """Remove a product from the cart.

        Args:
            discord_id (str): The ID of the discord account.
            product_id (str): The ID of the product to remove.
        """
        self.execute_and_check_errors("DLXEDD_CART", "remove", [discord_id, product_id])

    def cart_list(self, discord_id:str) -> list[dict]:
        """Get a list with all the products of the cart.

        Args:
            discord_id (str): The discord ID of the cart's account.

        Returns:
            list[dict]: A list of dictionaries repersenting the cart with the products in it.
        """
        lst = self.execute_and_check_errors("DLXEDD_CART", "list", [discord_id])
        return lst["data"]