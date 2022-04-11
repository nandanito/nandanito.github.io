---
layout: post
title: Easiest way to reset GIT repository
excerpt: "Follow these instructions to reset the repository rather than replacing with new one."
modified: 2013-01-10
category: notes
tags: [Programming]
comments: true
share: true
---

Sometimes you want/need to reset the `git` folder to complete new code. Rather than simply removing the folder and repository and creating new one, the following method solves the problem in couple of minutes. Follow the instructions, of course, at your own risk! I can simply assure you that I used it and it worked in my case.

<!--more-->

### So here it goes

If you aren't in the same folder as your _older_ code or you don't have your code at all, then get it first!

{% highlight bash %}
git pull origin master
{% endhighlight %}

To be sure that your are in _master_, `git checkout` to _master_. Then name the branch for the code, which you won't need anymore _(in this case, it is called __`old_stuff`__)_. Though it is not that necessary, it is recommended. In the end, push this branch to `origin`.

{% highlight bash %}
git checkout master
git branch old_stuff
git push origin old_stuff
{% endhighlight %}

Now change to a new branch that you want to use _(called __`new_stuff`__ here)_

{% highlight bash %}
git checkout -b new_stuff
{% endhighlight %}

Now you are ready to remove all the old files you don't need anymore

{% highlight bash %}
ls | xargs rm -rf
{% endhighlight %}

Copy new files, which you are going to use, in the same folder

{% highlight bash %}
cp -r {SOURCE_LOCATION} .
{% endhighlight %}

Add all the new copied files to git

{% highlight bash %}
git add -A
{% endhighlight %}

Commit and push your new branch to `origin`

{% highlight bash %}
git commit
git push origin new_stuff
{% endhighlight %}

Now update `master` for newer branch

{% highlight bash %}
git push . HEAD:master
{% endhighlight %}

Finally, push the newer version of _master_ to `origin`

{% highlight bash %}
git push origin master
{% endhighlight %}

That's all. You had just reset your `git`, while still having your older code as `old_stuff` branch on remote `origin`. You can remove that branch anytime you want or keep it for future reviews.

_Disclaimer:_ I am not responsible, if it creates any harm to your code or project. I would recommend you to understand each step, before you apply it. Best Luck!!!
