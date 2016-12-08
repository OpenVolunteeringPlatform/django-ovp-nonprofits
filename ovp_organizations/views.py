from ovp_users.models import User

from ovp_organizations import serializers
from ovp_organizations import models
from ovp_organizations import permissions as organization_permissions

from rest_framework import decorators
from rest_framework import viewsets
from rest_framework import response
from rest_framework import mixins
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404

#POST, PUT, PATCH -> /public-profile
#-criar perfil publico
#-editar perfil publico
#-convidar outro usuario pra organização
#-sair da organização
#-email
#
#GET -> /public-profile/:pk
class OrganizationResourceViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
  """
  OrganizationResourceViewSet resource endpoint
  """
  queryset = models.Organization.objects.all()
  lookup_field = 'slug'
  lookup_value_regex = '[^/]+' # default is [^/.]+ - here we're allowing dots in the url slug field

  @decorators.detail_route(methods=["POST"])
  def invite_user(self, request, *args, **kwargs):
    organization = self.get_object()

    serializer = self.get_serializer_class()(data=request.data)
    serializer.is_valid(raise_exception=True)

    invited = User.objects.get(email=request.data["email"])

    try:
      models.OrganizationInvite.objects.get(organization=organization, invited=invited)
      return response.Response({"email": ["This user is already invited to this organization."]}, status=400)
    except models.OrganizationInvite.DoesNotExist:
      pass

    invite = models.OrganizationInvite(invitator=request.user, invited=invited, organization=organization)
    invite.save()
    return response.Response({"detail": "User invited."})


  @decorators.detail_route(methods=["POST"])
  def join(self, request, *args, **kwargs):
    organization = self.get_object()
    organization.members.add(request.user)

    return response.Response({"detail": "Joined organization."})

  def get_serializer_class(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      return serializers.OrganizationCreateSerializer
    if self.action == 'retrieve':
      return serializers.OrganizationRetrieveSerializer
    if self.action == 'invite_user':
      return serializers.OrganizationInviteSerializer


  def get_permissions(self):
    request = self.get_serializer_context()['request']
    if self.action == 'create':
      self.permission_classes = (permissions.IsAuthenticated,)
    if self.action == 'retrieve':
      self.permission_classes = ()
    if self.action == 'invite_user':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.OwnsOrIsOrganizationMember)
    if self.action == 'join':
      self.permission_classes = (permissions.IsAuthenticated, organization_permissions.IsInvitedToOrganization)

    return super(OrganizationResourceViewSet, self).get_permissions()

  def create(self, request, *args, **kwargs):
    request.data['owner'] = request.user.id

    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    organization = serializer.save()
    organization.members.add(request.user)

    headers = self.get_success_headers(serializer.data)
    return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
