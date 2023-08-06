# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s lapis.member -t test_forum_page.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src lapis.member.testing.LAPIS_MEMBER_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/lapis/member/tests/robot/test_forum_page.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Forum Page
  Given a logged-in site administrator
    and an add Forum Page form
   When I type 'My Forum Page' into the title field
    and I submit the form
   Then a Forum Page with the title 'My Forum Page' has been created

Scenario: As a site administrator I can view a Forum Page
  Given a logged-in site administrator
    and a Forum Page 'My Forum Page'
   When I go to the Forum Page view
   Then I can see the Forum Page title 'My Forum Page'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Forum Page form
  Go To  ${PLONE_URL}/++add++Forum Page

a Forum Page 'My Forum Page'
  Create content  type=Forum Page  id=my-forum_page  title=My Forum Page

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Forum Page view
  Go To  ${PLONE_URL}/my-forum_page
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Forum Page with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Forum Page title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
