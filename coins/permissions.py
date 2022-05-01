from rest_framework import permissions


 
class TradePermission(permissions.BasePermission):
    '''
        permission check for user can trade or not
    '''
    def has_permission(self, request, view):
        return request.user.can_trade